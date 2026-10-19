"""Reproducible BQ2 model comparison."""
from pathlib import Path
import json
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, KFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data/Crop_Yield_original.csv'; TARGET='Crop_Yield_ton_per_hectare'; SEED=20261011
IDS={'baseline':'A056','crop_mean_baseline':'A061','linear_regression':'A057','random_forest':'A058','gradient_boosting':'A059','feature_contribution':'A060'}
def mets(y,p): return {'MAE':mean_absolute_error(y,p),'RMSE':mean_squared_error(y,p)**0.5,'R2':r2_score(y,p)}
def main():
    df=pd.read_csv(DATA); X=df.drop(columns=[TARGET]); y=df[TARGET]
    cats=X.select_dtypes(include=['object','category']).columns.tolist(); nums=[c for c in X if c not in cats]
    prep=ColumnTransformer([('cat',OneHotEncoder(handle_unknown='ignore',sparse_output=False),cats),('num','passthrough',nums)])
    specs={'baseline':DummyRegressor(strategy='mean'),'linear_regression':LinearRegression(),'random_forest':RandomForestRegressor(n_estimators=80,min_samples_leaf=2,random_state=SEED,n_jobs=1),'gradient_boosting':HistGradientBoostingRegressor(max_iter=150,learning_rate=.05,max_leaf_nodes=31,random_state=SEED)}
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=SEED,stratify=df['Crop_Type']); cv=KFold(5,shuffle=True,random_state=SEED); rows=[]
    # Training-only crop-mean benchmark: each test row receives its Crop_Type mean
    # calculated from Xtr/ytr; unseen categories fall back to the training global mean.
    crop_means=pd.DataFrame({'crop':Xtr['Crop_Type'],'target':ytr}).groupby('crop')['target'].mean()
    crop_pred=Xte['Crop_Type'].map(crop_means).fillna(ytr.mean())
    cm=mets(yte,crop_pred); rows.append({'Analysis_ID':IDS['crop_mean_baseline'],'model':'crop_mean_baseline','n_train':len(ytr),'n_test':len(yte),'train_MAE':None,'train_RMSE':None,'train_R2':None,'cv_MAE_mean':None,'cv_MAE_sd':None,'cv_RMSE_mean':None,'cv_RMSE_sd':None,'cv_R2_mean':None,'cv_R2_sd':None,'holdout_MAE':cm['MAE'],'holdout_RMSE':cm['RMSE'],'holdout_R2':cm['R2'],'seed':SEED,'status':'UNVERIFIED'})
    for crop in sorted(Xte['Crop_Type'].unique()):
        mask=Xte['Crop_Type'].eq(crop); cmm=mets(yte[mask],crop_pred[mask]); rows.append({'Analysis_ID':IDS['crop_mean_baseline'],'model':'crop_holdout','crop':crop,'n_test':int(mask.sum()),'holdout_MAE':cmm['MAE'],'holdout_RMSE':cmm['RMSE'],'holdout_R2':cmm['R2'],'status':'UNVERIFIED'})
    for name,est in specs.items():
        pipe=est if name=='baseline' else Pipeline([('preprocess',prep),('model',est)]); pipe.fit(Xtr,ytr); tr=mets(ytr,pipe.predict(Xtr)); te=mets(yte,pipe.predict(Xte)); sc={'MAE':'neg_mean_absolute_error','RMSE':'neg_root_mean_squared_error','R2':'r2'}; cr=cross_validate(pipe,Xtr,ytr,cv=cv,scoring=sc,n_jobs=1)
        rows.append({'Analysis_ID':IDS[name],'model':name,'n_train':len(ytr),'n_test':len(yte),'train_MAE':tr['MAE'],'train_RMSE':tr['RMSE'],'train_R2':tr['R2'],'cv_MAE_mean':-cr['test_MAE'].mean(),'cv_MAE_sd':cr['test_MAE'].std(ddof=1),'cv_RMSE_mean':-cr['test_RMSE'].mean(),'cv_RMSE_sd':cr['test_RMSE'].std(ddof=1),'cv_R2_mean':cr['test_R2'].mean(),'cv_R2_sd':cr['test_R2'].std(ddof=1),'holdout_MAE':te['MAE'],'holdout_RMSE':te['RMSE'],'holdout_R2':te['R2'],'seed':SEED,'status':'UNVERIFIED'})
        for crop in sorted(Xte['Crop_Type'].unique()):
            mask=Xte['Crop_Type'].eq(crop); cm=mets(yte[mask],pipe.predict(Xte[mask])); rows.append({'Analysis_ID':IDS[name],'model':'crop_holdout','crop':crop,'n_test':int(mask.sum()),'holdout_MAE':cm['MAE'],'holdout_RMSE':cm['RMSE'],'holdout_R2':cm['R2'],'status':'UNVERIFIED'})
        if name=='random_forest':
            pi=permutation_importance(pipe,Xte,yte,scoring='neg_root_mean_squared_error',n_repeats=10,random_state=SEED,n_jobs=1)
            for f,v,s in zip(X.columns,pi.importances_mean,pi.importances_std): rows.append({'Analysis_ID':IDS['feature_contribution'],'model':'permutation_importance','feature':f,'importance_mean':v,'importance_sd':s,'source_model':name,'status':'UNVERIFIED'})
    out=ROOT/'results'; pd.DataFrame(rows).to_csv(out/'model_metrics.csv',index=False)
    cfg={'seed':SEED,'test_size':.2,'cv_folds':5,'target':TARGET,'predictors':list(X.columns),'categorical':cats,'numeric':nums,'leakage_safeguards':['target excluded','split before preprocessing','preprocessing fitted inside folds'],'status':'UNVERIFIED'}; (out/'model_configuration.json').write_text(json.dumps(cfg,indent=2))
    reg=out/'analysis_register.csv'; old=pd.read_csv(reg); old=old[~old.analysis_id.isin([IDS['baseline'],IDS['crop_mean_baseline'],IDS['linear_regression'],IDS['random_forest'],IDS['gradient_boosting'],IDS['feature_contribution']])]; add=pd.DataFrame([{'analysis_id':i,'business_question':'BQ2','analysis_purpose':p,'dataset':'data/Crop_Yield_original.csv','variables':TARGET,'method':m,'n':len(df),'code_location':'analysis/phase5_bq2_modelling.py','output_location':'results/model_metrics.csv','statistical_result':'See results/model_metrics.csv','interpretation':'Predictive performance only; not causal.','final_status':'UNVERIFIED'} for i,p,m in [(IDS['baseline'],'Global mean prediction benchmark','DummyRegressor'),(IDS['linear_regression'],'Linear benchmark','One-hot linear regression pipeline'),(IDS['random_forest'],'Random Forest benchmark','RandomForestRegressor pipeline'),(IDS['gradient_boosting'],'Gradient boosting benchmark','HistGradientBoostingRegressor pipeline'),(IDS['feature_contribution'],'Predictive feature contribution','Holdout permutation importance'),(IDS['crop_mean_baseline'],'Training-only crop mean benchmark','Crop_Type means fitted on training partition')]]); old=pd.concat([old,add.reindex(columns=old.columns,fill_value='')],ignore_index=True); old.to_csv(reg,index=False)
if __name__=='__main__': main()

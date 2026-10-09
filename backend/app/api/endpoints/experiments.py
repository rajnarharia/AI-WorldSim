from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import models, database
from app.simulation.experiment_runner import ExperimentRunner

router = APIRouter()

@router.post("")
def create_experiment(name: str, population: int = 30, runs: int = 3, duration_days: int = 2, db: Session = Depends(database.get_db)):
    runner = ExperimentRunner(db)
    models_config = {"Model A": 34, "Model B": 33, "Model C": 33}
    exp = runner.create_experiment(name, population, runs, duration_days, models_config)
    return {"id": exp.id, "name": exp.name, "population": exp.population_size}

@router.get("")
def get_experiments(db: Session = Depends(database.get_db)):
    return db.query(models.Experiment).order_by(models.Experiment.id.desc()).all()

@router.get("/{exp_id}")
def get_experiment(exp_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Experiment).filter(models.Experiment.id == exp_id).first()

@router.post("/{exp_id}/run")
def run_experiment(exp_id: int, db: Session = Depends(database.get_db)):
    runner = ExperimentRunner(db)
    runner.run_experiment(exp_id)
    return {"status": "success"}

@router.post("/{exp_id}/start")
def start_experiment(exp_id: int, db: Session = Depends(database.get_db)):
    runner = ExperimentRunner(db)
    runner.run_experiment(exp_id)
    return {"status": "success"}

@router.post("/{exp_id}/pause")
def pause_experiment(exp_id: int, db: Session = Depends(database.get_db)):
    return {"status": "paused"}

@router.post("/{exp_id}/resume")
def resume_experiment(exp_id: int, db: Session = Depends(database.get_db)):
    return {"status": "resumed"}

@router.post("/{exp_id}/stop")
def stop_experiment(exp_id: int, db: Session = Depends(database.get_db)):
    return {"status": "stopped"}

@router.get("/{exp_id}/models")
def get_experiment_models(exp_id: int, db: Session = Depends(database.get_db)):
    assignments = db.query(models.ExperimentModelAssignment).filter(models.ExperimentModelAssignment.experiment_id == exp_id).all()
    return assignments

@router.get("/{exp_id}/metrics")
def get_experiment_metrics(exp_id: int, db: Session = Depends(database.get_db)):
    runs = db.query(models.ExperimentRun).filter(models.ExperimentRun.experiment_id == exp_id).all()
    run_ids = [r.id for r in runs]
    metrics = db.query(models.MetricResult).filter(models.MetricResult.run_id.in_(run_ids)).all()
    return metrics

@router.get("/{exp_id}/events")
def get_experiment_events(exp_id: int, db: Session = Depends(database.get_db)):
    runs = db.query(models.ExperimentRun).filter(models.ExperimentRun.experiment_id == exp_id).all()
    run_ids = [r.id for r in runs]
    events = db.query(models.EventLog).filter(models.EventLog.run_id.in_(run_ids)).all()
    return events

@router.get("/{exp_id}/cross-model-interactions")
def get_cmi(exp_id: int, db: Session = Depends(database.get_db)):
    cmis = db.query(models.CrossModelInteraction).filter(models.CrossModelInteraction.experiment_id == exp_id).all()
    matrix = {}
    for c in cmis:
        src = c.source_model_id or "Unknown"
        tgt = c.target_model_id or "Unknown"
        if src not in matrix: matrix[src] = {}
        if tgt not in matrix[src]: matrix[src][tgt] = 0
        matrix[src][tgt] += 1
    return matrix

@router.get("/{exp_id}/comparison")
def get_model_comparison(exp_id: int, db: Session = Depends(database.get_db)):
    runs = db.query(models.ExperimentRun).filter(models.ExperimentRun.experiment_id == exp_id).all()
    run_ids = [r.id for r in runs]
    
    results = db.query(
        models.MetricResult.metric_name, 
        models.MetricResult.model_type,
        func.avg(models.MetricResult.metric_value).label('mean'),
        func.max(models.MetricResult.metric_value).label('max'),
        func.min(models.MetricResult.metric_value).label('min')
    ).filter(
        models.MetricResult.run_id.in_(run_ids),
        models.MetricResult.model_type != None
    ).group_by(models.MetricResult.metric_name, models.MetricResult.model_type).all()
    
    comparison = {}
    for r in results:
        if r.metric_name not in comparison:
            comparison[r.metric_name] = {}
        comparison[r.metric_name][r.model_type] = {
            "mean": round(r.mean, 2),
            "max": round(r.max, 2),
            "min": round(r.min, 2)
        }
    return comparison

from app.simulation.final_analysis_engine import FinalAnalysisEngine
from fastapi.responses import JSONResponse, Response, StreamingResponse
from fastapi import HTTPException
import csv
import io
import json

@router.post("/{exp_id}/generate-report")
def generate_report(exp_id: int, db: Session = Depends(database.get_db)):
    engine = FinalAnalysisEngine(db, exp_id)
    try:
        report = engine.generate_full_report()
        return {"status": "success", "report_id": report.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{exp_id}/report")
def get_report(exp_id: int, db: Session = Depends(database.get_db)):
    report = db.query(models.ExperimentReport).filter(models.ExperimentReport.experiment_id == exp_id).order_by(models.ExperimentReport.report_version.desc()).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return {
        "id": report.id,
        "experiment_id": report.experiment_id,
        "generated_at": report.generated_at,
        "version": report.report_version,
        "overview": json.loads(report.overview or '{}'),
        "safety_analysis": json.loads(report.safety_analysis or '{}'),
        "economic_analysis": json.loads(report.economic_analysis or '{}'),
        "social_analysis": json.loads(report.social_analysis or '{}'),
        "governance_analysis": json.loads(report.governance_analysis or '{}'),
        "ai_behaviour_analysis": json.loads(report.ai_behaviour_analysis or '{}'),
        "cross_model_analysis": json.loads(report.cross_model_analysis or '{}'),
        "important_events": json.loads(report.important_events or '[]'),
        "findings": json.loads(report.findings or '[]'),
        "limitations": json.loads(report.limitations or '[]'),
        "conclusion": report.conclusion
    }

@router.get("/{exp_id}/analysis")
def get_analysis(exp_id: int, db: Session = Depends(database.get_db)):
    report = db.query(models.ExperimentReport).filter(models.ExperimentReport.experiment_id == exp_id).order_by(models.ExperimentReport.report_version.desc()).first()
    if not report: raise HTTPException(status_code=404, detail="Report not found")
    return {
        "safety": json.loads(report.safety_analysis or '{}'),
        "economic": json.loads(report.economic_analysis or '{}'),
        "social": json.loads(report.social_analysis or '{}'),
        "governance": json.loads(report.governance_analysis or '{}'),
        "ai_behaviour": json.loads(report.ai_behaviour_analysis or '{}'),
    }

@router.get("/{exp_id}/findings")
def get_findings(exp_id: int, db: Session = Depends(database.get_db)):
    report = db.query(models.ExperimentReport).filter(models.ExperimentReport.experiment_id == exp_id).order_by(models.ExperimentReport.report_version.desc()).first()
    if not report: raise HTTPException(status_code=404, detail="Report not found")
    return json.loads(report.findings or '[]')

@router.get("/{exp_id}/limitations")
def get_limitations(exp_id: int, db: Session = Depends(database.get_db)):
    report = db.query(models.ExperimentReport).filter(models.ExperimentReport.experiment_id == exp_id).order_by(models.ExperimentReport.report_version.desc()).first()
    if not report: raise HTTPException(status_code=404, detail="Report not found")
    return json.loads(report.limitations or '[]')

@router.get("/{exp_id}/export/json")
def export_json(exp_id: int, db: Session = Depends(database.get_db)):
    report = db.query(models.ExperimentReport).filter(models.ExperimentReport.experiment_id == exp_id).order_by(models.ExperimentReport.report_version.desc()).first()
    if not report: raise HTTPException(status_code=404, detail="Report not found")
    
    data = {
        "experiment_id": report.experiment_id,
        "overview": json.loads(report.overview or '{}'),
        "findings": json.loads(report.findings or '[]'),
        "conclusion": report.conclusion
    }
    return JSONResponse(content=data, headers={"Content-Disposition": f"attachment; filename=\"report_{exp_id}.json\""})

@router.get("/{exp_id}/export/csv")
def export_csv(exp_id: int, db: Session = Depends(database.get_db)):
    runs = db.query(models.ExperimentRun).filter(models.ExperimentRun.experiment_id == exp_id).all()
    run_ids = [r.id for r in runs]
    metrics = db.query(models.MetricResult).filter(models.MetricResult.run_id.in_(run_ids)).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["tick", "simulation_day", "category", "metric_name", "model_type", "metric_value"])
    for m in metrics:
        writer.writerow([m.tick, m.simulation_day, m.category, m.metric_name, m.model_type, m.metric_value])
        
    response = Response(content=output.getvalue(), media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename=\"metrics_{exp_id}.csv\""
    return response

@router.get("/{exp_id}/export/pdf")
def export_pdf(exp_id: int, db: Session = Depends(database.get_db)):
    report = db.query(models.ExperimentReport).filter(models.ExperimentReport.experiment_id == exp_id).order_by(models.ExperimentReport.report_version.desc()).first()
    if not report: raise HTTPException(status_code=404, detail="Report not found")
    
    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="AI WorldSim Final Report", ln=1, align="C")
        pdf.cell(200, 10, txt=f"Experiment ID: {exp_id}", ln=1, align="C")
        pdf.multi_cell(0, 10, txt=f"Conclusion: {report.conclusion}")
        
        pdf_bytes = bytes(pdf.output())
        return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=\"report_{exp_id}.pdf\""})
    except ImportError:
        text = f"AI WorldSim Final Report\nExperiment ID: {exp_id}\nConclusion:\n{report.conclusion}\n"
        return Response(content=text, media_type="text/plain", headers={"Content-Disposition": f"attachment; filename=\"report_{exp_id}.txt\""})

# Validación 'Dry Run' (Sin Ejecución)

| Script | Estado Técnico | Detalle |
|--------|----------------|---------|
| `analyze_postgres_laws.py` | VALID | Syntax OK |
| `analyze_qdrant_laws.py` | VALID | Syntax OK |
| `anonymize_content.py` | VALID | Syntax OK |
| `backend/__init__.py` | VALID | Syntax OK |
| `backend/calcular_tamano_rag.py` | VALID | Syntax OK |
| `backend/check_db_status.py` | VALID | Syntax OK |
| `backend/check_status_v2.py` | VALID | Syntax OK |
| `backend/database/db.py` | VALID | Syntax OK |
| `backend/database/init_db.py` | VALID | Syntax OK |
| `backend/expand_rag_system.py` | VALID | Syntax OK |
| `backend/migrate_qdrant_to_cloud.py` | BROKEN_IMPORTS | Missing Imports: dotenv... |
| `backend/models/metadata_schema.py` | VALID | Syntax OK |
| `backend/routers/__init__.py` | VALID | Syntax OK |
| `backend/routers/ai_functions.py` | BROKEN_IMPORTS | Missing Imports: fastapi, fastapi.responses, genanki... |
| `backend/routers/boe.py` | BROKEN_IMPORTS | Missing Imports: fastapi, boe_api_client... |
| `backend/routers/chat.py` | BROKEN_IMPORTS | Missing Imports: fastapi, fastapi.responses, agents.rag_agent_v2... |
| `backend/routers/mcp_gateway.py` | BROKEN_IMPORTS | Missing Imports: fastapi... |
| `backend/routers/rag.py` | BROKEN_IMPORTS | Missing Imports: fastapi, agents.rag_agent_v2... |
| `backend/routers/rag_v2.py` | BROKEN_IMPORTS | Missing Imports: fastapi, agents.rag_agent_v2... |
| `backend/routers/upload.py` | BROKEN_IMPORTS | Missing Imports: fastapi, pypdf... |
| `backend/routers/user.py` | BROKEN_IMPORTS | Missing Imports: fastapi, database.db... |
| `backend/scripts/1_export_local.py` | VALID | Syntax OK |
| `backend/scripts/2_create_cloud_collection.py` | BROKEN_IMPORTS | Missing Imports: dotenv... |
| `backend/scripts/3_import_to_cloud.py` | BROKEN_IMPORTS | Missing Imports: dotenv... |
| `backend/scripts/check_qdrant_status.py` | VALID | Syntax OK |
| `backend/scripts/ingest_scraped_rd84.py` | VALID | Syntax OK |
| `backend/scripts/ingest_scraped_universal.py` | VALID | Syntax OK |
| `backend/scripts/modify_mcp_index.py` | VALID | Syntax OK |
| `backend/scripts/verify_ingestion_rd84.py` | VALID | Syntax OK |
| `backend/scripts/verify_ingestion_universal.py` | VALID | Syntax OK |
| `backend/stats_por_norma.py` | VALID | Syntax OK |
| `backend/utils/scrape_boe_rd84.py` | BROKEN_IMPORTS | Missing Imports: bs4... |
| `backend/utils/scrape_boe_universal.py` | BROKEN_IMPORTS | Missing Imports: bs4... |
| `backend/verificar_qdrant.py` | VALID | Syntax OK |
| `basura/backend/check_articulo_168.py` | VALID | Syntax OK |
| `basura/backend/delete_and_reindex_constitucion.py` | BROKEN_IMPORTS | Missing Imports: pypdf... |
| `basura/backend/download_sprint3.py` | VALID | Syntax OK |
| `basura/backend/download_sprint4.py` | VALID | Syntax OK |
| `basura/backend/index_capa3_restantes.py` | BROKEN_IMPORTS | Missing Imports: agents.pdf_processor, agents.robertalex_embedder, agents.indexer... |
| `basura/backend/index_constitucion.py` | BROKEN_IMPORTS | Missing Imports: agents.indexer, agents.pdf_processor, agents.robertalex_embedder... |
| `basura/backend/index_lgss_complete.py` | BROKEN_IMPORTS | Missing Imports: agents.indexer... |
| `basura/backend/index_sprint3.py` | BROKEN_IMPORTS | Missing Imports: agents.pdf_processor, agents.robertalex_embedder, agents.indexer... |
| `basura/backend/index_sprint4.py` | BROKEN_IMPORTS | Missing Imports: agents.pdf_processor, agents.robertalex_embedder, agents.indexer... |
| `basura/backend/verificacion_completa_sistema.py` | VALID | Syntax OK |
| `basura/backend/verify_3_leyes_criticas.py` | VALID | Syntax OK |
| `basura/backend/verify_articulo_168_final.py` | VALID | Syntax OK |
| `basura/backend/verify_before_sprint3.py` | VALID | Syntax OK |
| `basura/backend/verify_constitucion.py` | VALID | Syntax OK |
| `basura/backend/verify_constitucion_pdf.py` | BROKEN_IMPORTS | Missing Imports: pypdf... |
| `basura/backend/verify_pdf_constitucion.py` | BROKEN_IMPORTS | Missing Imports: pypdf... |
| `basura/backend/verify_rd_cotizacion.py` | VALID | Syntax OK |
| `check_qdrant.py` | VALID | Syntax OK |
| `clean_pii_datasets.py` | VALID | Syntax OK |
| `completar_simulacro.py` | VALID | Syntax OK |
| `consolidate_datasets.py` | VALID | Syntax OK |
| `dataset_generator/agents/__init__.py` | BROKEN_IMPORTS | Missing Imports: simulacro_agent... |
| `dataset_generator/agents/simulacro_agent/__init__.py` | VALID | Syntax OK |
| `dataset_generator/agents/simulacro_agent/mcp_client.py` | VALID | Syntax OK |
| `dataset_generator/agents/simulacro_agent/simulacro_agent.py` | VALID | Syntax OK |
| `dataset_generator/analizar_dificultad_examenes.py` | VALID | Syntax OK |
| `dataset_generator/analizar_dificultad_simple.py` | VALID | Syntax OK |
| `dataset_generator/analyze_duplicates.py` | BROKEN_IMPORTS | Missing Imports: PyPDF2... |
| `dataset_generator/audit_boe_quality.py` | VALID | Syntax OK |
| `dataset_generator/check_collections.py` | VALID | Syntax OK |
| `dataset_generator/check_payload_structure.py` | VALID | Syntax OK |
| `dataset_generator/comparar_calidad_qa.py` | VALID | Syntax OK |
| `dataset_generator/comparar_todos_modelos.py` | VALID | Syntax OK |
| `dataset_generator/consolidar_dataset_final.py` | VALID | Syntax OK |
| `dataset_generator/export_dataset.py` | VALID | Syntax OK |
| `dataset_generator/extract_text.py` | BROKEN_IMPORTS | Missing Imports: PyPDF2, pdfplumber... |
| `dataset_generator/generar_10_maxdif_simple.py` | VALID | Syntax OK |
| `dataset_generator/generar_qa_3_prueba.py` | VALID | Syntax OK |
| `dataset_generator/generar_qa_claude.py` | VALID | Syntax OK |
| `dataset_generator/generar_qa_claude_kiro_10.py` | VALID | Syntax OK |
| `dataset_generator/generar_qa_cohere.py` | VALID | Syntax OK |
| `dataset_generator/generar_qa_deepseek.py` | BROKEN_IMPORTS | Missing Imports: dotenv... |
| `dataset_generator/generar_qa_groq.py` | VALID | Syntax OK |
| `dataset_generator/generar_qa_kimi.py` | VALID | Syntax OK |
| `dataset_generator/generar_qa_mistral_api.py` | VALID | Syntax OK |
| `dataset_generator/generar_qa_mistral_local.py` | VALID | Syntax OK |
| `dataset_generator/generar_qa_mistral_local_20.py` | VALID | Syntax OK |
| `dataset_generator/generar_qa_prueba_rapida.py` | VALID | Syntax OK |
| `dataset_generator/generate_flashcards.py` | BROKEN_IMPORTS | Missing Imports: dotenv... |
| `dataset_generator/generate_premium_cases.py` | BROKEN_IMPORTS | Missing Imports: dotenv... |
| `dataset_generator/generate_qa.py` | BROKEN_IMPORTS | Missing Imports: dotenv, groq, anthropic... |
| `dataset_generator/generate_qa_advanced_agent.py` | BROKEN_IMPORTS | Missing Imports: dotenv... |
| `dataset_generator/generate_qa_multi_model_v1.py` | BROKEN_IMPORTS | Missing Imports: dotenv... |
| `dataset_generator/groq_batch_service.py` | BROKEN_IMPORTS | Missing Imports: dotenv... |
| `dataset_generator/human_review.py` | VALID | Syntax OK |
| `dataset_generator/indexar_materiales_bge_m3.py` | VALID | Syntax OK |
| `dataset_generator/pipeline_ollama_local.py` | BROKEN_IMPORTS | Missing Imports: PyPDF2... |
| `dataset_generator/pipeline_seguro_local.py` | BROKEN_IMPORTS | Missing Imports: PyPDF2... |
| `dataset_generator/prepare_groq_batch_500.py` | VALID | Syntax OK |
| `dataset_generator/process_groq_batch.py` | VALID | Syntax OK |
| `dataset_generator/run_pipeline.py` | VALID | Syntax OK |
| `dataset_generator/scan_materiales_academia.py` | VALID | Syntax OK |
| `dataset_generator/url_verifier.py` | VALID | Syntax OK |
| `dataset_generator/verify_boe_links.py` | BROKEN_IMPORTS | Missing Imports: bs4... |
| `dataset_generator/verify_qa.py` | BROKEN_IMPORTS | Missing Imports: dotenv, groq... |
| `extract_conceptual_materials.py` | BROKEN_IMPORTS | Missing Imports: pytesseract, pdf2image... |
| `extract_remaining_exams.py` | BROKEN_IMPORTS | Missing Imports: pytesseract, pdf2image... |
| `extract_with_ocr.py` | BROKEN_IMPORTS | Missing Imports: pytesseract, pdf2image... |
| `generate_10_qa_agentic.py` | BROKEN_IMPORTS | Missing Imports: dotenv, groq... |
| `generate_conceptual_qa_hybrid.py` | VALID | Syntax OK |
| `generate_mass_qa_v2.py` | BROKEN_IMPORTS | Missing Imports: mistralai... |
| `generate_premium_qa.py` | VALID | Syntax OK |
| `generate_premium_qa_batch2.py` | VALID | Syntax OK |
| `generate_premium_qa_batch3.py` | VALID | Syntax OK |
| `generate_qa_agentic_complete.py` | BROKEN_IMPORTS | Missing Imports: dotenv, groq... |
| `generate_qa_agentic_direct.py` | BROKEN_IMPORTS | Missing Imports: dotenv, groq... |
| `generate_qa_mistral_real.py` | BROKEN_IMPORTS | Missing Imports: mistralai... |
| `generate_report.py` | VALID | Syntax OK |
| `improve_mistral_qa.py` | VALID | Syntax OK |
| `improve_ocr_quality.py` | BROKEN_IMPORTS | Missing Imports: pytesseract, pdf2image... |
| `improve_ocr_remaining.py` | BROKEN_IMPORTS | Missing Imports: pytesseract, pdf2image... |
| `orchestrate_generation.py` | VALID | Syntax OK |
| `pair_questions_answers.py` | VALID | Syntax OK |
| `parse_answer_sheet.py` | VALID | Syntax OK |
| `parse_exam_questions.py` | VALID | Syntax OK |
| `repair_dataset_refs.py` | VALID | Syntax OK |
| `scripts_20_12/generate_10_qa_mistral_studio.py` | BROKEN_IMPORTS | Missing Imports: mistralai... |
| `scripts_20_12/generate_10_qa_mistral_v2.py` | BROKEN_IMPORTS | Missing Imports: mistralai... |
| `verify_dataset_quality.py` | VALID | Syntax OK |
| `verify_mass_qa.py` | VALID | Syntax OK |

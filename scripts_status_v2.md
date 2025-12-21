# Auditoría de Scripts - Fase 2 (Refinado)

| Script | Estado | Razón |
|--------|--------|-------|
| `analyze_postgres_laws.py` | UTILITY | Likely helper script |
| `analyze_qdrant_laws.py` | UTILITY | Likely helper script |
| `anonymize_content.py` | UTILITY | Likely helper script |
| `backend/__init__.py` | UTILITY | Likely helper script |
| `backend/agents/MAL_ingest_boe_4layers_extended.py` | ACTIVE | Protected System File |
| `backend/agents/__init__.py` | ACTIVE | Protected System File |
| `backend/agents/boe_api_client.py` | ACTIVE | Protected System File |
| `backend/agents/boe_downloader.py` | ACTIVE | Protected System File |
| `backend/agents/indexar_materiales_academia.py` | ACTIVE | Protected System File |
| `backend/agents/indexer.py` | ACTIVE | Protected System File |
| `backend/agents/ingest_hybrid_two_tier.py` | ACTIVE | Protected System File |
| `backend/agents/ingest_missing_4_laws.py` | ACTIVE | Protected System File |
| `backend/agents/llm_providers.py` | ACTIVE | Protected System File |
| `backend/agents/mistral_tools.py` | ACTIVE | Protected System File |
| `backend/agents/pdf_processor.py` | ACTIVE | Protected System File |
| `backend/agents/rag_agent.py` | ACTIVE | Protected System File |
| `backend/agents/rag_agent_v2.py` | ACTIVE | Protected System File |
| `backend/agents/setup_semantic_cache.py` | ACTIVE | Protected System File |
| `backend/calcular_tamano_rag.py` | UTILITY | Likely helper script |
| `backend/check_db_status.py` | UTILITY | Likely helper script |
| `backend/check_status_v2.py` | UTILITY | Likely helper script |
| `backend/database/db.py` | UTILITY | Likely helper script |
| `backend/database/init_db.py` | UTILITY | Likely helper script |
| `backend/expand_rag_system.py` | UTILITY | Likely helper script |
| `backend/main.py` | ACTIVE | Protected System File |
| `backend/migrate_qdrant_to_cloud.py` | UTILITY | Likely helper script |
| `backend/models/metadata_schema.py` | UTILITY | Likely helper script |
| `backend/routers/__init__.py` | UTILITY | Likely helper script |
| `backend/routers/ai_functions.py` | UTILITY | Likely helper script |
| `backend/routers/boe.py` | UTILITY | Likely helper script |
| `backend/routers/chat.py` | UTILITY | Likely helper script |
| `backend/routers/mcp_gateway.py` | UTILITY | Likely helper script |
| `backend/routers/rag.py` | UTILITY | Likely helper script |
| `backend/routers/rag_v2.py` | UTILITY | Likely helper script |
| `backend/routers/upload.py` | UTILITY | Likely helper script |
| `backend/routers/user.py` | UTILITY | Likely helper script |
| `backend/scripts/1_export_local.py` | UTILITY | Likely helper script |
| `backend/scripts/2_create_cloud_collection.py` | UTILITY | Likely helper script |
| `backend/scripts/3_import_to_cloud.py` | UTILITY | Likely helper script |
| `backend/scripts/check_qdrant_status.py` | UTILITY | Likely helper script |
| `backend/scripts/ingest_scraped_rd84.py` | UTILITY | Likely helper script |
| `backend/scripts/ingest_scraped_universal.py` | UTILITY | Likely helper script |
| `backend/scripts/modify_mcp_index.py` | UTILITY | Likely helper script |
| `backend/scripts/verify_ingestion_rd84.py` | UTILITY | Likely helper script |
| `backend/scripts/verify_ingestion_universal.py` | UTILITY | Likely helper script |
| `backend/setup_qdrant_collection.py` | CONFIG | Configuration |
| `backend/stats_por_norma.py` | UTILITY | Likely helper script |
| `backend/test_ai_functions.py` | TEST/DEBUG | Test file |
| `backend/test_all_providers.py` | TEST/DEBUG | Test file |
| `backend/test_database.py` | TEST/DEBUG | Test file |
| `backend/test_db_integration.py` | TEST/DEBUG | Test file |
| `backend/test_simple.py` | TEST/DEBUG | Test file |
| `backend/test_user_router.py` | TEST/DEBUG | Test file |
| `backend/tests/__init__.py` | TEST | Test file |
| `backend/tests/test_chat.py` | TEST/DEBUG | Test file |
| `backend/tests/test_mistral_tools.py` | TEST/DEBUG | Test file |
| `backend/tests/test_performance.py` | TEST/DEBUG | Test file |
| `backend/tests/test_upload.py` | TEST/DEBUG | Test file |
| `backend/utils/scrape_boe_rd84.py` | UTILITY | Likely helper script |
| `backend/utils/scrape_boe_universal.py` | UTILITY | Likely helper script |
| `backend/verificar_qdrant.py` | UTILITY | Likely helper script |
| `basura/backend/check_articulo_168.py` | UTILITY | Likely helper script |
| `basura/backend/delete_and_reindex_constitucion.py` | UTILITY | Likely helper script |
| `basura/backend/download_sprint3.py` | UTILITY | Likely helper script |
| `basura/backend/download_sprint4.py` | UTILITY | Likely helper script |
| `basura/backend/index_capa3_restantes.py` | UTILITY | Likely helper script |
| `basura/backend/index_capa3_tests.py` | TEST/DEBUG | Test file |
| `basura/backend/index_constitucion.py` | UTILITY | Likely helper script |
| `basura/backend/index_lgss_complete.py` | UTILITY | Likely helper script |
| `basura/backend/index_sprint3.py` | UTILITY | Likely helper script |
| `basura/backend/index_sprint4.py` | UTILITY | Likely helper script |
| `basura/backend/test_chat_completo.py` | TEST/DEBUG | Test file |
| `basura/backend/test_chat_frontend.py` | TEST/DEBUG | Test file |
| `basura/backend/test_constitucion.py` | TEST/DEBUG | Test file |
| `basura/backend/test_import.py` | TEST/DEBUG | Test file |
| `basura/backend/test_mistral_rag.py` | TEST/DEBUG | Test file |
| `basura/backend/test_rag_completo.py` | TEST/DEBUG | Test file |
| `basura/backend/test_reranking.py` | TEST/DEBUG | Test file |
| `basura/backend/test_robertalex_local.py` | TEST/DEBUG | Test file |
| `basura/backend/test_setup.py` | TEST/DEBUG | Test file |
| `basura/backend/verificacion_completa_sistema.py` | UTILITY | Likely helper script |
| `basura/backend/verify_3_leyes_criticas.py` | UTILITY | Likely helper script |
| `basura/backend/verify_and_setup.py` | CONFIG | Configuration |
| `basura/backend/verify_articulo_168_final.py` | UTILITY | Likely helper script |
| `basura/backend/verify_before_sprint3.py` | UTILITY | Likely helper script |
| `basura/backend/verify_constitucion.py` | UTILITY | Likely helper script |
| `basura/backend/verify_constitucion_pdf.py` | UTILITY | Likely helper script |
| `basura/backend/verify_pdf_constitucion.py` | UTILITY | Likely helper script |
| `basura/backend/verify_rd_cotizacion.py` | UTILITY | Likely helper script |
| `check_qdrant.py` | UTILITY | Likely helper script |
| `clean_pii_datasets.py` | UTILITY | Likely helper script |
| `completar_simulacro.py` | UTILITY | Likely helper script |
| `consolidate_datasets.py` | UTILITY | Likely helper script |
| `dataset_generator/agents/__init__.py` | UTILITY | Likely helper script |
| `dataset_generator/agents/simulacro_agent/__init__.py` | UTILITY | Likely helper script |
| `dataset_generator/agents/simulacro_agent/mcp_client.py` | UTILITY | Likely helper script |
| `dataset_generator/agents/simulacro_agent/simulacro_agent.py` | UTILITY | Likely helper script |
| `dataset_generator/agents/simulacro_agent/test_generator.py` | TEST/DEBUG | Test file |
| `dataset_generator/analizar_dificultad_examenes.py` | UTILITY | Likely helper script |
| `dataset_generator/analizar_dificultad_simple.py` | UTILITY | Likely helper script |
| `dataset_generator/analyze_duplicates.py` | UTILITY | Likely helper script |
| `dataset_generator/audit_boe_quality.py` | UTILITY | Likely helper script |
| `dataset_generator/check_collections.py` | UTILITY | Likely helper script |
| `dataset_generator/check_payload_structure.py` | UTILITY | Likely helper script |
| `dataset_generator/comparar_calidad_qa.py` | UTILITY | Likely helper script |
| `dataset_generator/comparar_todos_modelos.py` | UTILITY | Likely helper script |
| `dataset_generator/consolidar_dataset_final.py` | UTILITY | Likely helper script |
| `dataset_generator/debug_qdrant.py` | TEST/DEBUG | Test file |
| `dataset_generator/export_dataset.py` | UTILITY | Likely helper script |
| `dataset_generator/extract_text.py` | UTILITY | Likely helper script |
| `dataset_generator/generar_10_maxdif_simple.py` | UTILITY | Likely helper script |
| `dataset_generator/generar_qa_3_prueba.py` | UTILITY | Likely helper script |
| `dataset_generator/generar_qa_claude.py` | UTILITY | Likely helper script |
| `dataset_generator/generar_qa_claude_kiro_10.py` | UTILITY | Likely helper script |
| `dataset_generator/generar_qa_cohere.py` | UTILITY | Likely helper script |
| `dataset_generator/generar_qa_deepseek.py` | UTILITY | Likely helper script |
| `dataset_generator/generar_qa_groq.py` | UTILITY | Likely helper script |
| `dataset_generator/generar_qa_kimi.py` | UTILITY | Likely helper script |
| `dataset_generator/generar_qa_mistral_api.py` | UTILITY | Likely helper script |
| `dataset_generator/generar_qa_mistral_local.py` | UTILITY | Likely helper script |
| `dataset_generator/generar_qa_mistral_local_20.py` | UTILITY | Likely helper script |
| `dataset_generator/generar_qa_prueba_rapida.py` | UTILITY | Likely helper script |
| `dataset_generator/generate_flashcards.py` | UTILITY | Likely helper script |
| `dataset_generator/generate_premium_cases.py` | UTILITY | Likely helper script |
| `dataset_generator/generate_qa.py` | LEGACY (Old Gen) | Old Generation Script |
| `dataset_generator/generate_qa_advanced_agent.py` | LEGACY (Old Gen) | Old Generation Script |
| `dataset_generator/generate_qa_multi_model_v1.py` | LEGACY (Old Gen) | Old Generation Script |
| `dataset_generator/groq_batch_service.py` | UTILITY | Likely helper script |
| `dataset_generator/human_review.py` | UTILITY | Likely helper script |
| `dataset_generator/indexar_materiales_bge_m3.py` | UTILITY | Likely helper script |
| `dataset_generator/pipeline_ollama_local.py` | UTILITY | Likely helper script |
| `dataset_generator/pipeline_seguro_local.py` | UTILITY | Likely helper script |
| `dataset_generator/prepare_groq_batch_500.py` | UTILITY | Likely helper script |
| `dataset_generator/process_groq_batch.py` | UTILITY | Likely helper script |
| `dataset_generator/run_pipeline.py` | UTILITY | Likely helper script |
| `dataset_generator/scan_materiales_academia.py` | UTILITY | Likely helper script |
| `dataset_generator/test_deepseek_structure.py` | TEST/DEBUG | Test file |
| `dataset_generator/test_deepseek_types.py` | TEST/DEBUG | Test file |
| `dataset_generator/test_dependencies.py` | TEST/DEBUG | Test file |
| `dataset_generator/test_indexacion_simple.py` | TEST/DEBUG | Test file |
| `dataset_generator/test_qa_generation.py` | TEST/DEBUG | Test file |
| `dataset_generator/test_qdrant_search.py` | TEST/DEBUG | Test file |
| `dataset_generator/test_qdrant_simple.py` | TEST/DEBUG | Test file |
| `dataset_generator/url_verifier.py` | UTILITY | Likely helper script |
| `dataset_generator/verify_boe_links.py` | UTILITY | Likely helper script |
| `dataset_generator/verify_qa.py` | UTILITY | Likely helper script |
| `debug_rag_scores.py` | TEST/DEBUG | Test file |
| `extract_conceptual_materials.py` | UTILITY | Likely helper script |
| `extract_remaining_exams.py` | UTILITY | Likely helper script |
| `extract_with_ocr.py` | UTILITY | Likely helper script |
| `generate_10_qa_agentic.py` | LEGACY (Old Gen) | Old Generation Script |
| `generate_cases_deepseek.py` | ACTIVE (GOLD) | Core Generation Script |
| `generate_cases_groq.py` | ACTIVE (GOLD) | Core Generation Script |
| `generate_cases_mistral.py` | ACTIVE (GOLD) | Core Generation Script |
| `generate_conceptual_qa_hybrid.py` | LEGACY (Old Gen) | Old Generation Script |
| `generate_mass_qa_v2.py` | LEGACY (Old Gen) | Old Generation Script |
| `generate_premium_qa.py` | LEGACY (Old Gen) | Old Generation Script |
| `generate_premium_qa_batch2.py` | LEGACY (Old Gen) | Old Generation Script |
| `generate_premium_qa_batch3.py` | LEGACY (Old Gen) | Old Generation Script |
| `generate_qa_agentic_complete.py` | LEGACY (Old Gen) | Old Generation Script |
| `generate_qa_agentic_direct.py` | LEGACY (Old Gen) | Old Generation Script |
| `generate_qa_mistral_real.py` | LEGACY (Old Gen) | Old Generation Script |
| `generate_report.py` | UTILITY | Likely helper script |
| `improve_mistral_qa.py` | UTILITY | Likely helper script |
| `improve_ocr_quality.py` | UTILITY | Likely helper script |
| `improve_ocr_remaining.py` | UTILITY | Likely helper script |
| `orchestrate_generation.py` | UTILITY | Likely helper script |
| `pair_questions_answers.py` | UTILITY | Likely helper script |
| `parse_answer_sheet.py` | UTILITY | Likely helper script |
| `parse_exam_questions.py` | UTILITY | Likely helper script |
| `repair_dataset_refs.py` | UTILITY | Likely helper script |
| `scripts/maintenance/analyze_academy_duplicates.py` | ACTIVE | Protected System File |
| `scripts/maintenance/check_qdrant_status.py` | ACTIVE | Protected System File |
| `scripts/maintenance/comparar_qdrant_local_vs_cloud.py` | ACTIVE | Protected System File |
| `scripts/maintenance/crear_indice_norma.py` | ACTIVE | Protected System File |
| `scripts/maintenance/detectar_leyes_faltantes.py` | ACTIVE | Protected System File |
| `scripts/maintenance/extract_exams.py` | ACTIVE | Protected System File |
| `scripts/maintenance/generate_qa_from_schemas.py` | ACTIVE | Protected System File |
| `scripts/maintenance/limpiar_qdrant_cloud.py` | ACTIVE | Protected System File |
| `scripts/maintenance/monitorear_indexacion.py` | ACTIVE | Protected System File |
| `scripts/maintenance/url_verifier.py` | ACTIVE | Protected System File |
| `scripts/maintenance/verificacion_completa_qdrant.py` | ACTIVE | Protected System File |
| `scripts/maintenance/verificar_estado_completo.py` | ACTIVE | Protected System File |
| `scripts/maintenance/verificar_leyes_temario_oficial.py` | ACTIVE | Protected System File |
| `scripts/maintenance/verificar_qdrant_cloud.py` | ACTIVE | Protected System File |
| `scripts/tests/test_agente_2_preguntas_dificiles.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_agente_mistral_simple.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_claude_final.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_e2e_completo.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_e2e_simple.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_imv_final.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_mistral_agent.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_mistral_agent_complete.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_mistral_agent_quality_check.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_mistral_agent_respuestas_completas.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_mistral_agent_single.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_mistral_agent_tools.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_mistral_chat_verificacion.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_mistral_nueva_key.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_mistral_only.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_mistral_pipeline.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_mistral_vs_claude.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_mock_exam_generation.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_qdrant_cloud_e2e.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_rag_leyes_nuevas.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_rag_simple.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_simple_comparison.py` | TEST/DEBUG | Test file |
| `scripts/tests/test_url_verifier.py` | TEST/DEBUG | Test file |
| `scripts_20_12/generate_10_qa_mistral_studio.py` | LEGACY (Old Gen) | Old Generation Script |
| `scripts_20_12/generate_10_qa_mistral_v2.py` | LEGACY (Old Gen) | Old Generation Script |
| `test_claude_models.py` | TEST/DEBUG | Test file |
| `test_claude_structured.py` | TEST/DEBUG | Test file |
| `test_mistral_agent_simple.py` | TEST/DEBUG | Test file |
| `test_rag_mistral.py` | TEST/DEBUG | Test file |
| `verify_dataset_quality.py` | UTILITY | Likely helper script |
| `verify_mass_qa.py` | UTILITY | Likely helper script |

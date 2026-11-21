# Dokumentation und Setup: Vollstaendigkeitsabgleich

Statischer Repository-Abgleich des lokalen Standes. Zeitpunkt/Commit separat festhalten. Neu erzeugen:

```text
python -B scripts/audit_tool_coverage.py --output docs/TOOL_SETUP_AUDIT.md
```

**Nein, nicht alle dokumentierten Werkzeuge sind als installierbare Tools integriert.**
Dieser Bericht liest nur Repository-Dateien, startet weder Setup noch WSL und prueft
keine tatsaechlich installierte Software, Downloads, Builds, Provider oder Dienste.

## Ergebnis

| Messwert | Anzahl |
|---|---|
| Gelesene Markdown-Dateien (Bericht selbst ausgenommen) | 1396 |
| Registry-Eintraege | 441 |
| Explizite Tools-Menueeintraege | 400 |
| Registry ohne Tools-Menueeintrag | 138 |
| Tools-Menue ohne Registry-Zuordnung | 97 |
| Registry mit bekanntem Installationsplatzhalter | 134 |
| Rezepte im separaten Entwicklungskatalog | 62 |
| Quellen im Entwicklungskatalog | 62 |
| Eindeutige GitHub-Repositories in der Dokumentation | 711 |
| GitHub-Referenzen ohne direkte Quellenzuordnung | 302 |

## So sind die Ergebnisse zu lesen

- Hauptmenue 8 zeigt die Tools-Liste aus setup_ultimate.sh plus der bekannten nativen Allowlist, nicht automatisch die Registry.
- Die 62 Entwicklungsquellen sind separat ueber Hauptmenue 16 bzw. die Zusatzschaltflaeche im Tools-Menue erreichbar.
- Registry-only bedeutet nicht automatisch fehlender Installer: alternative Skripte/Projektwege separat pruefen.
- Ein vorhandenes Skript beweist weder eine vollstaendige Installation noch eine nutzbare Runtime. Source-only, VSIX, manuelle Downloads und optionale Builds bleiben unterschiedliche Modi.
- Ein bekannter Platzhalter ist kein Installer. Status planned kann aber auch bei einem echten Skript veraltet sein.
- GitHub-Referenzen umfassen Bibliotheken, Actions, Modelle, Mirrors und Beispiele. Nicht zugeordnete Referenzen sind Pruefkandidaten, keine automatische Liste fehlender Programme.
- Verglichen werden literale Bash-Arrays/Mappings, die bekannte native Menue-Ergaenzung und direkte Quellen-URLs. Andere dynamische Shell-Logik wird nicht ausgefuehrt; historische Aliase und indirekte Helper-URLs sind nicht vollstaendig semantisch aufloesbar.
- Keine Installationsbereitschaft aus einem Dateinamen ableiten; diesen Bericht nicht als Live-Abnahme verwenden.

## Registry ohne Eintrag im Tools-Menue

| ID | Installationsweg | Umfang |
|---|---|---|
| lightrag | scripts/tools/lightrag_install.sh | Skript vorhanden; Runtime ungeprueft |
| ufw | scripts/tools/ufw_install.sh | Skript vorhanden; Runtime ungeprueft |
| tailscale | scripts/tools/tailscale_install.sh | Skript vorhanden; Runtime ungeprueft |
| esphome | scripts/tools/esphome_install.sh | Skript vorhanden; Runtime ungeprueft |
| borgbackup | scripts/tools/borgbackup_install.sh | Skript vorhanden; Runtime ungeprueft |
| clamav | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| yara | scripts/tools/yara_install.sh | Skript vorhanden; Runtime ungeprueft |
| haystack | scripts/tools/haystack_install.sh | Skript vorhanden; Runtime ungeprueft |
| pytest | scripts/tools/pytest_install.sh | Skript vorhanden; Runtime ungeprueft |
| deepeval | scripts/tools/deepeval_install.sh | Skript vorhanden; Runtime ungeprueft |
| pihole | scripts/tools/pihole_install.sh | Skript vorhanden; Runtime ungeprueft |
| adguard_home | scripts/tools/adguard_home_install.sh | Skript vorhanden; Runtime ungeprueft |
| trafilatura | scripts/tools/trafilatura_install.sh | Skript vorhanden; Runtime ungeprueft |
| reuse | scripts/tools/reuse_install.sh | Skript vorhanden; Runtime ungeprueft |
| scancode_toolkit | scripts/tools/scancode_toolkit_install.sh | Skript vorhanden; Runtime ungeprueft |
| gbox | scripts/tools/gbox_install.sh | Skript vorhanden; Runtime ungeprueft |
| stalwart_mail | scripts/tools/stalwart_mail_install.sh | Skript vorhanden; Runtime ungeprueft |
| queue_manager | scripts/tools/queue_manager_install.sh | Skript vorhanden; Runtime ungeprueft |
| tasktiger | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| rq | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| celery | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| dramatiq | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| bullmq | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| swe_agent | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| cosign | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| sops | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| age | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| suricata | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| wazuh | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| headscale | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| headplane | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| wireguard | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| frp | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| nginx_proxy_manager | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| ddclient_he | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| acme_sh | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| rspamd | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| roundcube | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| snappymail | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mailpit | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| opendkim | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| opendmarc | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| kopia | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| supabase_self_hosted | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| duplicati | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| automatic1111 | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| krita_ai_diffusion | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| job_queue | scripts/tools/job_queue_install.sh | Skript vorhanden; Runtime ungeprueft |
| modelcontextprotocol_servers | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mcp_filesystem | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mcp_git | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mcp_github | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mcp_shell | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mcp_browser | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mcp_sqlite | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mcp_postgres | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mcp_fetch | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mcp_memory | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| supervisord | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| systemd_user_units | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| tmux | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| pm2 | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| lynis | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| openscap | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mcp_filesystem_server | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mcp_git_server | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mcp_github_server | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mcp_shell_server | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mcp_browser_server | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mcp_sqlite_server | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mcp_postgres_server | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mcp_fetch_server | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mcp_memory_server | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| styletts2 | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| openvoice | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| seed_vc | scripts/tools/seed_vc_install.sh | Skript vorhanden; Runtime ungeprueft |
| diffsinger | scripts/tools/diffsinger_install.sh | Skript vorhanden; Runtime ungeprueft |
| openutau | scripts/tools/openutau_install.sh | Skript vorhanden; Runtime ungeprueft |
| nnsvs | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| fish_speech | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| melotts | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| kokoro_tts | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| spark_tts | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| hallo2 | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| emo_avatar | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| skyreels_a1 | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| wav2lip | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| clearer_voice_studio | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| subtitleedit | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| openbao | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| infisical | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| glances | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| blocky | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| localai | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| browsermcp | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| docker_mcp_registry | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| pass | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| litestream | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| fastlane | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| apktool | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mitmproxy | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| radicale | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| imap_importer | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| git | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| doctor | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| wsl2 | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| voice_studio | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| podcast_studio | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| audiobook_studio | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| dubbing_studio | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| prompt_generator_studio | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| video_ai_production | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| character_library | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| voice_clone | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| ai_choir | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| android_sdk | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| gradle | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| jadx | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| arq | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| apscheduler | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| renovate | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| check_resource_budget | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| mkdocs | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| firejail | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| wakeonlan | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| nvidia_smi | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| ddclient | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| check_tools | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| check_profiles | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| check_ports | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| paddleocr | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| livekit | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| asterisk | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| beszel | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| zeek | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| falco | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| stalwart | scripts/tools/planned_tool_stub_install.sh | Platzhalter |
| sieve | scripts/tools/planned_tool_stub_install.sh | Platzhalter |

## Tools-Menue ohne Registry-Zuordnung

| Menueeintrag | Tatsaechliches Skript | Umfang |
|---|---|---|
| Actionlint | scripts/tools/actionlint_install.sh | Skript vorhanden; Runtime ungeprueft |
| Agent_Router | scripts/tools/agent_router_install.sh | Skript vorhanden; Runtime ungeprueft |
| Ahrefs | scripts/tools/ahrefs_install.sh | Skript vorhanden; Runtime ungeprueft |
| AI_Powered_Law_Firms | scripts/tools/ai_powered_law_firms_install.sh | Skript vorhanden; Runtime ungeprueft |
| Airtable | scripts/tools/airtable_install.sh | Skript vorhanden; Runtime ungeprueft |
| AnimateDiff | scripts/tools/animatediff_install.sh | Skript vorhanden; Runtime ungeprueft |
| Axolotl | scripts/tools/axolotl_install.sh | Skript vorhanden; Runtime ungeprueft |
| Backtest_Workflow | scripts/tools/backtest_workflow_install.sh | Skript vorhanden; Runtime ungeprueft |
| BPM_Analyzer | scripts/tools/bpm_analyzer_install.sh | Skript vorhanden; Runtime ungeprueft |
| Browser_Tool | scripts/tools/browser_tool_install.sh | Skript vorhanden; Runtime ungeprueft |
| Buffer_API | scripts/tools/buffer_api_install.sh | Skript vorhanden; Runtime ungeprueft |
| Clawbake | scripts/tools/clawbake_install.sh | Skript vorhanden; Runtime ungeprueft |
| Clawhub | scripts/tools/clawhub_install.sh | Skript vorhanden; Runtime ungeprueft |
| Clawhub_CLI | scripts/tools/clawhub_cli_install.sh | Skript vorhanden; Runtime ungeprueft |
| Code_Sandbox | scripts/tools/code_sandbox_install.sh | Skript vorhanden; Runtime ungeprueft |
| ControlNet | scripts/tools/controlnet_install.sh | Skript vorhanden; Runtime ungeprueft |
| Data_Juicer | scripts/tools/data_juicer_install.sh | Skript vorhanden; Runtime ungeprueft |
| Deadline_Checker | scripts/tools/deadline_checker_install.sh | Skript vorhanden; Runtime ungeprueft |
| Docker_Compose_Plugin | scripts/tools/docker_compose_plugin_install.sh | Skript vorhanden; Runtime ungeprueft |
| Drafting_Agent | scripts/tools/drafting_agent_install.sh | Skript vorhanden; Runtime ungeprueft |
| ElevenLabs | scripts/tools/elevenlabs_install.sh | Skript vorhanden; Runtime ungeprueft |
| Emotion_Tagging | scripts/tools/emotion_tagging_install.sh | Skript vorhanden; Runtime ungeprueft |
| EnviroLLM | scripts/tools/envirollm_install.sh | Skript vorhanden; Runtime ungeprueft |
| Ethers_JS | scripts/tools/ethers_js_install.sh | Skript vorhanden; Runtime ungeprueft |
| EULLM | scripts/tools/eullm_install.sh | Skript vorhanden; Runtime ungeprueft |
| Exchange_APIs | scripts/tools/exchange_apis_install.sh | Skript vorhanden; Runtime ungeprueft |
| Fail2Ban_Analyzer | scripts/tools/fail2ban_analyzer_install.sh | Skript vorhanden; Runtime ungeprueft |
| File_System_Tool | scripts/tools/file_system_tool_install.sh | Skript vorhanden; Runtime ungeprueft |
| FinGPT | scripts/tools/fingpt_install.sh | Skript vorhanden; Runtime ungeprueft |
| Fooocus | scripts/tools/fooocus_install.sh | Skript vorhanden; Runtime ungeprueft |
| Foundry | scripts/tools/foundry_install.sh | Skript vorhanden; Runtime ungeprueft |
| GitHub_API_Tooling | scripts/tools/github_api_tooling_install.sh | Skript vorhanden; Runtime ungeprueft |
| GitHub_Research | scripts/tools/github_research_install.sh | Skript vorhanden; Runtime ungeprueft |
| Google_Analytics_API | scripts/tools/google_analytics_api_install.sh | Skript vorhanden; Runtime ungeprueft |
| Hadolint | scripts/tools/hadolint_install.sh | Skript vorhanden; Runtime ungeprueft |
| Hardhat | scripts/tools/hardhat_install.sh | Skript vorhanden; Runtime ungeprueft |
| Hook_Detection | scripts/tools/hook_detection_install.sh | Skript vorhanden; Runtime ungeprueft |
| HubSpot | scripts/tools/hubspot_install.sh | Skript vorhanden; Runtime ungeprueft |
| Huge_Facing | scripts/tools/huge_facing_install.sh | Skript vorhanden; Runtime ungeprueft |
| Image_Upscaler_Pipeline | scripts/tools/image_upscaler_pipeline_install.sh | Skript vorhanden; Runtime ungeprueft |
| Joplin_CLI | scripts/tools/joplin_cli_install.sh | Skript vorhanden; Runtime ungeprueft |
| Kimi2 | scripts/tools/kimi2_install.sh | Skript vorhanden; Runtime ungeprueft |
| Kubectx_Kubens | scripts/tools/kubectx_kubens_install.sh | Skript vorhanden; Runtime ungeprueft |
| Kubernetes | scripts/tools/kubernetes_install.sh | Skript vorhanden; Runtime ungeprueft |
| Lawfirm | scripts/tools/lawfirm_install.sh | Skript vorhanden; Runtime ungeprueft |
| LibreOffice_Headless | scripts/tools/libreoffice_headless_install.sh | Skript vorhanden; Runtime ungeprueft |
| librosa | scripts/tools/librosa_install.sh | Skript vorhanden; Runtime ungeprueft |
| Llama_CPP_Toolchain | scripts/tools/llama_cpp_toolchain_install.sh | Skript vorhanden; Runtime ungeprueft |
| LLaMA_Factory | scripts/tools/llama_factory_install.sh | Skript vorhanden; Runtime ungeprueft |
| Make | scripts/tools/make_automation_install.sh | Skript vorhanden; Runtime ungeprueft |
| Memory_Policies | scripts/tools/memory_policies_install.sh | Skript vorhanden; Runtime ungeprueft |
| Meta_Ads_API | scripts/tools/meta_ads_api_install.sh | Skript vorhanden; Runtime ungeprueft |
| MLflow | scripts/tools/mlflow_install.sh | Skript vorhanden; Runtime ungeprueft |
| Music2P_Pipeline | scripts/tools/music2p_pipeline_install.sh | Skript vorhanden; Runtime ungeprueft |
| NATS | scripts/tools/nats_install.sh | Skript vorhanden; Runtime ungeprueft |
| Nikto | scripts/tools/nikto_install.sh | Skript vorhanden; Runtime ungeprueft |
| Notion | scripts/tools/notion_install.sh | Skript vorhanden; Runtime ungeprueft |
| OPA | scripts/tools/opa_install.sh | Skript vorhanden; Runtime ungeprueft |
| OpenClaw_RL | scripts/tools/openclaw_rl_install.sh | Skript vorhanden; Runtime ungeprueft |
| OpenManus | scripts/tools/openmanus_install.sh | Skript vorhanden; Runtime ungeprueft |
| PDF_Parser | scripts/tools/pdf_parser_install.sh | Skript vorhanden; Runtime ungeprueft |
| Pgvector | scripts/tools/pgvector_install.sh | Skript vorhanden; Runtime ungeprueft |
| Pipedream | scripts/tools/pipedream_install.sh | Skript vorhanden; Runtime ungeprueft |
| pydub | scripts/tools/pydub_install.sh | Skript vorhanden; Runtime ungeprueft |
| Ray | scripts/tools/ray_install.sh | Skript vorhanden; Runtime ungeprueft |
| Repo_Comparison | scripts/tools/repo_comparison_install.sh | Skript vorhanden; Runtime ungeprueft |
| Riffusion | scripts/tools/riffusion_install.sh | Skript vorhanden; Runtime ungeprueft |
| Risk_Agent | scripts/tools/risk_agent_install.sh | Skript vorhanden; Runtime ungeprueft |
| Risk_Scoring | scripts/tools/risk_scoring_install.sh | Skript vorhanden; Runtime ungeprueft |
| Risk_Strategy_Analyzer | scripts/tools/risk_strategy_analyzer_install.sh | Skript vorhanden; Runtime ungeprueft |
| Runway_API | scripts/tools/runway_api_install.sh | Skript vorhanden; Runtime ungeprueft |
| Security_Workflow | scripts/tools/security_workflow_install.sh | Skript vorhanden; Runtime ungeprueft |
| SEMrush | scripts/tools/semrush_install.sh | Skript vorhanden; Runtime ungeprueft |
| SQLite | scripts/tools/sqlite_install.sh | Skript vorhanden; Runtime ungeprueft |
| SQLite_Vec | scripts/tools/sqlite_vec_install.sh | Skript vorhanden; Runtime ungeprueft |
| Stable_Diffusion_WebUI | scripts/tools/stable_diffusion_webui_install.sh | Skript vorhanden; Runtime ungeprueft |
| Suno_API | scripts/tools/suno_api_install.sh | Skript vorhanden; Runtime ungeprueft |
| SVD | scripts/tools/svd_install.sh | Skript vorhanden; Runtime ungeprueft |
| Tax_Calculator | scripts/tools/tax_calculator_install.sh | Skript vorhanden; Runtime ungeprueft |
| Tax_Law_Agent | scripts/tools/tax_law_agent_install.sh | Skript vorhanden; Runtime ungeprueft |
| Thumbnail_Pipeline | scripts/tools/thumbnail_pipeline_install.sh | Skript vorhanden; Runtime ungeprueft |
| TikTok_Ads_API | scripts/tools/tiktok_ads_api_install.sh | Skript vorhanden; Runtime ungeprueft |
| TikTok_Score | scripts/tools/tiktok_score_install.sh | Skript vorhanden; Runtime ungeprueft |
| Trend_Monitor | scripts/tools/trend_monitor_install.sh | Skript vorhanden; Runtime ungeprueft |
| Udio_API | scripts/tools/udio_api_install.sh | Skript vorhanden; Runtime ungeprueft |
| Unsloth | scripts/tools/unsloth_install.sh | Skript vorhanden; Runtime ungeprueft |
| Upload_Automation | scripts/tools/upload_automation_install.sh | Skript vorhanden; Runtime ungeprueft |
| Voice_Assistant_Runtime | scripts/tools/voice_assistant_runtime_install.sh | Skript vorhanden; Runtime ungeprueft |
| VS_Code_Server | scripts/tools/vs_code_server_install.sh | Skript vorhanden; Runtime ungeprueft |
| Web3_APIs | scripts/tools/web3_apis_install.sh | Skript vorhanden; Runtime ungeprueft |
| Web3_Py | scripts/tools/web3_py_install.sh | Skript vorhanden; Runtime ungeprueft |
| Weights_and_Biases | scripts/tools/weights_and_biases_install.sh | Skript vorhanden; Runtime ungeprueft |
| Whisper | scripts/tools/whisper_install.sh | Skript vorhanden; Runtime ungeprueft |
| YT_DLP | scripts/tools/yt_dlp_install.sh | Skript vorhanden; Runtime ungeprueft |
| Zapier | scripts/tools/zapier_install.sh | Skript vorhanden; Runtime ungeprueft |
| Zenbot_API | scripts/tools/zenbot_api_install.sh | Skript vorhanden; Runtime ungeprueft |
| Zenbot_trader | scripts/tools/zenbot_trader_install.sh | Skript vorhanden; Runtime ungeprueft |

## Alle Registry-Eintraege

| ID | Tools-Menue | Status / Modus | Installationsskript / Umfang |
|---|---|---|---|
| cert_manager | cert-manager | experimental / github-native-build | scripts/tools/cert_manager_install.sh: Skript vorhanden; Runtime ungeprueft |
| external_dns | External_DNS | experimental / github-native-build | scripts/tools/external_dns_install.sh: Skript vorhanden; Runtime ungeprueft |
| kyverno | Kyverno | experimental / github-native-build | scripts/tools/kyverno_install.sh: Skript vorhanden; Runtime ungeprueft |
| gatekeeper | Gatekeeper | experimental / github-native-build | scripts/tools/gatekeeper_install.sh: Skript vorhanden; Runtime ungeprueft |
| keda | KEDA | experimental / github-native-build | scripts/tools/keda_install.sh: Skript vorhanden; Runtime ungeprueft |
| phoenix | Arize_Phoenix | experimental / github-native-build | scripts/tools/phoenix_install.sh: Skript vorhanden; Runtime ungeprueft |
| valkey | Valkey | experimental / github-native-build | scripts/tools/valkey_install.sh: Skript vorhanden; Runtime ungeprueft |
| gvisor | gVisor | experimental / github-native-build | scripts/tools/gvisor_install.sh: Skript vorhanden; Runtime ungeprueft |
| kata_containers | Kata_Containers | experimental / github-native-build | scripts/tools/kata_containers_install.sh: Skript vorhanden; Runtime ungeprueft |
| firecracker | Firecracker | experimental / github-native-build | scripts/tools/firecracker_install.sh: Skript vorhanden; Runtime ungeprueft |
| milvus | Milvus | experimental / github-native-build | scripts/tools/milvus_install.sh: Skript vorhanden; Runtime ungeprueft |
| kube_bench | Kube_Bench | experimental / github-native-build | scripts/tools/kube_bench_install.sh: Skript vorhanden; Runtime ungeprueft |
| kubescape | Kubescape | experimental / github-native-build | scripts/tools/kubescape_install.sh: Skript vorhanden; Runtime ungeprueft |
| nuclei | Nuclei | experimental / github-native-build | scripts/tools/nuclei_install.sh: Skript vorhanden; Runtime ungeprueft |
| testssl | Testssl | experimental / github-native-build | scripts/tools/testssl_install.sh: Skript vorhanden; Runtime ungeprueft |
| owasp_zap | OWASP_ZAP | experimental / github-native-build | scripts/tools/owasp_zap_install.sh: Skript vorhanden; Runtime ungeprueft |
| checkov | Checkov | experimental / github-native-build | scripts/tools/checkov_install.sh: Skript vorhanden; Runtime ungeprueft |
| ragas | Ragas | experimental / github-native-build | scripts/tools/ragas_install.sh: Skript vorhanden; Runtime ungeprueft |
| audile | Audile | experimental / github-source | scripts/tools/audile_install.sh: Skript vorhanden; Runtime ungeprueft |
| songrec | SongRec | experimental / github-source | scripts/tools/songrec_install.sh: Skript vorhanden; Runtime ungeprueft |
| mousai | Mousai | experimental / github-source | scripts/tools/mousai_install.sh: Skript vorhanden; Runtime ungeprueft |
| dejavu | Dejavu | experimental / github-source | scripts/tools/dejavu_install.sh: Skript vorhanden; Runtime ungeprueft |
| qwen3_235b | Qwen3_235B_A22B | experimental / github-source | scripts/tools/qwen3_235b_install.sh: Skript vorhanden; Runtime ungeprueft |
| qwq_32b | QwQ_32B | experimental / github-source | scripts/tools/qwq_32b_install.sh: Skript vorhanden; Runtime ungeprueft |
| gpt_oss_120b | GPT_OSS_120B | experimental / github-source | scripts/tools/gpt_oss_120b_install.sh: Skript vorhanden; Runtime ungeprueft |
| levo_2 | LeVo_2 | experimental / github-source | scripts/tools/levo_2_install.sh: Skript vorhanden; Runtime ungeprueft |
| moss_music | MOSS_Music | experimental / github-source | scripts/tools/moss_music_install.sh: Skript vorhanden; Runtime ungeprueft |
| poelm | PoeLM | experimental / github-source | scripts/tools/poelm_install.sh: Skript vorhanden; Runtime ungeprueft |
| poetone | PoeTone | experimental / github-source | scripts/tools/poetone_install.sh: Skript vorhanden; Runtime ungeprueft |
| copoet | CoPoet | experimental / github-source | scripts/tools/copoet_install.sh: Skript vorhanden; Runtime ungeprueft |
| ctgs | CTGS | experimental / github-source | scripts/tools/ctgs_install.sh: Skript vorhanden; Runtime ungeprueft |
| songsage | SongSage | planned / manual | scripts/tools/songsage_install.sh: Skript vorhanden; Runtime ungeprueft |
| outlines | Outlines | experimental / github-source | scripts/tools/outlines_install.sh: Skript vorhanden; Runtime ungeprueft |
| espeak_ng | eSpeak_NG | experimental / github-source | scripts/tools/espeak_ng_install.sh: Skript vorhanden; Runtime ungeprueft |
| qwen_coder | Qwen_Coder | experimental / github-source | scripts/tools/qwen_coder_install.sh: Skript vorhanden; Runtime ungeprueft |
| minimax_m3 | MiniMax_M3 | experimental / github-source | scripts/tools/minimax_m3_install.sh: Skript vorhanden; Runtime ungeprueft |
| obot | Obot | experimental / github-source | scripts/tools/obot_install.sh: Skript vorhanden; Runtime ungeprueft |
| deepseek_r1 | DeepSeek_R1 | experimental / github-source | scripts/tools/deepseek_r1_install.sh: Skript vorhanden; Runtime ungeprueft |
| codex_cli | Codex_CLI | experimental / source | scripts/tools/codex_cli_install.sh: Skript vorhanden; Runtime ungeprueft |
| gemini_desktop_bwendell | Gemini_Desktop_Bwendell | experimental / desktop-manual | scripts/tools/gemini_desktop_bwendell_install.sh: Skript vorhanden; Runtime ungeprueft |
| gemini_desktop_bwendell_source | Gemini_Desktop_Bwendell_Source | experimental / source | scripts/tools/gemini_desktop_bwendell_source_install.sh: Skript vorhanden; Runtime ungeprueft |
| gemini_desktop_dortanes | Gemini_Desktop_Dortanes_Legacy | experimental / desktop-manual | scripts/tools/gemini_desktop_dortanes_install.sh: Skript vorhanden; Runtime ungeprueft |
| gemini_desktop_dortanes_source | Gemini_Desktop_Dortanes_Source | experimental / source | scripts/tools/gemini_desktop_dortanes_source_install.sh: Skript vorhanden; Runtime ungeprueft |
| openapi_servers | OpenAPI_Servers | experimental / openapi-time | scripts/tools/openapi_servers_install.sh: Skript vorhanden; Runtime ungeprueft |
| godot_source | Godot_Source | experimental / source | scripts/tools/godot_source_install.sh: Skript vorhanden; Runtime ungeprueft |
| godot_build | Godot_Build | experimental / godot-build | scripts/tools/godot_build_install.sh: Skript vorhanden; Runtime ungeprueft |
| godot_xr_tools | Godot_XR_Tools | experimental / source | scripts/tools/godot_xr_tools_install.sh: Skript vorhanden; Runtime ungeprueft |
| o3de_source | O3DE_Source | experimental / source | scripts/tools/o3de_source_install.sh: Skript vorhanden; Runtime ungeprueft |
| lively_wallpaper_source | Lively_Wallpaper_Source | experimental / source | scripts/tools/lively_wallpaper_source_install.sh: Skript vorhanden; Runtime ungeprueft |
| qwen_desktop_study | Qwen_Desktop_Study | experimental / github-study-sources-optional-build | scripts/tools/qwen_desktop_study_install.sh: Skript vorhanden; Runtime ungeprueft |
| enki_browser_study | Enki_Browser_Study | experimental / github-study-sources-optional-packaging | scripts/tools/enki_browser_study_install.sh: Skript vorhanden; Runtime ungeprueft |
| browseros_study | BrowserOS_Study | experimental / github-study-sources-optional-build | scripts/tools/browseros_study_install.sh: Skript vorhanden; Runtime ungeprueft |
| comet | Comet | experimental / desktop-manual | scripts/tools/comet_install.sh: Skript vorhanden; Runtime ungeprueft |
| browseros | BrowserOS | experimental / desktop-manual | scripts/tools/browseros_install.sh: Skript vorhanden; Runtime ungeprueft |
| enki_browser | Enki_Browser | experimental / desktop-manual | scripts/tools/enki_browser_install.sh: Skript vorhanden; Runtime ungeprueft |
| browser_use | Browser_Use | experimental / browser-python | scripts/tools/browser_use_install.sh: Skript vorhanden; Runtime ungeprueft |
| perplexity_mcp | Perplexity_MCP | experimental / perplexity-mcp | scripts/tools/perplexity_mcp_install.sh: Skript vorhanden; Runtime ungeprueft |
| perplexity_python | Perplexity_Python | experimental / perplexity-python | scripts/tools/perplexity_python_install.sh: Skript vorhanden; Runtime ungeprueft |
| perplexity_node | Perplexity_Node | experimental / perplexity-node | scripts/tools/perplexity_node_install.sh: Skript vorhanden; Runtime ungeprueft |
| perplexity_cookbook | Perplexity_API_Cookbook | experimental / source | scripts/tools/perplexity_cookbook_install.sh: Skript vorhanden; Runtime ungeprueft |
| qwen_desktop_build | Qwen_Desktop_Build | experimental / github-desktop-build | scripts/tools/qwen_desktop_build_install.sh: Skript vorhanden; Runtime ungeprueft |
| hermes_agent_jarvis | Hermes_Agent_Jarvis | experimental / github-python-package | scripts/tools/hermes_agent_jarvis_install.sh: Skript vorhanden; Runtime ungeprueft |
| gradio | Gradio | experimental / github-source | scripts/tools/gradio_install.sh: Skript vorhanden; Runtime ungeprueft |
| streamlit | Streamlit | experimental / github-source | scripts/tools/streamlit_install.sh: Skript vorhanden; Runtime ungeprueft |
| concat | Concat | experimental / github-release-appimage | scripts/tools/concat_install.sh: Skript vorhanden; Runtime ungeprueft |
| remotion | Remotion | experimental / github-source-build | scripts/tools/remotion_install.sh: Skript vorhanden; Runtime ungeprueft |
| hyperframes | HyperFrames | experimental / github-source-build | scripts/tools/hyperframes_install.sh: Skript vorhanden; Runtime ungeprueft |
| openmontage | OpenMontage | experimental / github-python-core | scripts/tools/openmontage_install.sh: Skript vorhanden; Runtime ungeprueft |
| marp | Marp | experimental / github-release | scripts/tools/marp_install.sh: Skript vorhanden; Runtime ungeprueft |
| listmonk | Listmonk | experimental / github-release | scripts/tools/listmonk_install.sh: Skript vorhanden; Runtime ungeprueft |
| mautic | Mautic | experimental / github-release | scripts/tools/mautic_install.sh: Skript vorhanden; Runtime ungeprueft |
| gopls | Gopls | experimental / github-source-build | scripts/tools/gopls_install.sh: Skript vorhanden; Runtime ungeprueft |
| delve | Delve | experimental / github-source-build | scripts/tools/delve_install.sh: Skript vorhanden; Runtime ungeprueft |
| golangci_lint | GolangCI_Lint | experimental / github-source-build | scripts/tools/golangci_lint_install.sh: Skript vorhanden; Runtime ungeprueft |
| kubeconform | Kubeconform | experimental / github-source-build | scripts/tools/kubeconform_install.sh: Skript vorhanden; Runtime ungeprueft |
| kubelinter | KubeLinter | experimental / github-source-build | scripts/tools/kubelinter_install.sh: Skript vorhanden; Runtime ungeprueft |
| tflint | TFLint | experimental / github-source-build | scripts/tools/tflint_install.sh: Skript vorhanden; Runtime ungeprueft |
| terraform_docs | Terraform_Docs | experimental / github-source-build | scripts/tools/terraform_docs_install.sh: Skript vorhanden; Runtime ungeprueft |
| sqlfluff | SQLFluff | experimental / github-source-build | scripts/tools/sqlfluff_install.sh: Skript vorhanden; Runtime ungeprueft |
| bats_core | Bats_Core | experimental / github-scripts | scripts/tools/bats_core_install.sh: Skript vorhanden; Runtime ungeprueft |
| invoke_build | Invoke_Build | experimental / github-scripts | scripts/tools/invoke_build_install.sh: Skript vorhanden; Runtime ungeprueft |
| black | Black | experimental / github-source-build | scripts/tools/black_install.sh: Skript vorhanden; Runtime ungeprueft |
| mypy | Mypy | experimental / github-source-build | scripts/tools/mypy_install.sh: Skript vorhanden; Runtime ungeprueft |
| youtube_agent_skill | YouTube_Agent_Skill | experimental / github-skills-copy | scripts/tools/youtube_agent_skill_install.sh: Skript vorhanden; Runtime ungeprueft |
| anthropic_cli | Anthropic_CLI | experimental / github-source-build | scripts/tools/anthropic_cli_install.sh: Skript vorhanden; Runtime ungeprueft |
| agentic_os | Agentic_OS | experimental / github-source-only | scripts/tools/agentic_os_install.sh: Skript vorhanden; Runtime ungeprueft |
| colibri | Colibri | experimental / github-source-only | scripts/tools/colibri_install.sh: Skript vorhanden; Runtime ungeprueft |
| hyperfine | Hyperfine | experimental / github-source-only | scripts/tools/hyperfine_install.sh: Skript vorhanden; Runtime ungeprueft |
| hf_accelerate | HF_Accelerate | experimental / github-source-only | scripts/tools/hf_accelerate_install.sh: Skript vorhanden; Runtime ungeprueft |
| deepspeed | DeepSpeed | experimental / github-source-only | scripts/tools/deepspeed_install.sh: Skript vorhanden; Runtime ungeprueft |
| rea | REA | experimental / github-source-optional-build | scripts/tools/rea_install.sh: Skript vorhanden; Runtime ungeprueft |
| find_skills | Find_Skills | experimental / github-skill-copy | scripts/tools/find_skills_install.sh: Skript vorhanden; Runtime ungeprueft |
| claude_code | Claude_Code | experimental / source | scripts/tools/claude_code_install.sh: Skript vorhanden; Runtime ungeprueft |
| gemini_cli | Gemini_CLI | experimental / source | scripts/tools/gemini_cli_install.sh: Skript vorhanden; Runtime ungeprueft |
| qwen_desktop | Qwen_Desktop | planned / manual-windows | scripts/tools/qwen_desktop_install.sh: Skript vorhanden; Runtime ungeprueft |
| cline | Cline | experimental / github-release | scripts/tools/cline_install.sh: Skript vorhanden; Runtime ungeprueft |
| qwen_code | Qwen_Code | experimental / source | scripts/tools/qwen_code_install.sh: Skript vorhanden; Runtime ungeprueft |
| wan21 | Wan21 | experimental / source | scripts/tools/wan21_install.sh: Skript vorhanden; Runtime ungeprueft |
| comfyui_gguf | ComfyUI_GGUF | experimental / source | scripts/tools/comfyui_gguf_install.sh: Skript vorhanden; Runtime ungeprueft |
| wanvideo_wrapper | WanVideoWrapper | experimental / github-source | scripts/tools/wanvideowrapper_install.sh: Skript vorhanden; Runtime ungeprueft |
| supir | SUPIR | experimental / source | scripts/tools/supir_install.sh: Skript vorhanden; Runtime ungeprueft |
| film | FILM | experimental / source | scripts/tools/film_install.sh: Skript vorhanden; Runtime ungeprueft |
| pyannote_audio | Pyannote_Audio | experimental / source | scripts/tools/pyannote_audio_install.sh: Skript vorhanden; Runtime ungeprueft |
| deepfilternet | DeepFilterNet | experimental / source | scripts/tools/deepfilternet_install.sh: Skript vorhanden; Runtime ungeprueft |
| audioseal | AudioSeal | experimental / source | scripts/tools/audioseal_install.sh: Skript vorhanden; Runtime ungeprueft |
| cogvideox | CogVideoX | experimental / github-source | scripts/tools/cogvideox_install.sh: Skript vorhanden; Runtime ungeprueft |
| ltx_video | LTX_Video | experimental / github-source | scripts/tools/ltx_video_install.sh: Skript vorhanden; Runtime ungeprueft |
| tgi | TGI | experimental / source | scripts/tools/tgi_install.sh: Skript vorhanden; Runtime ungeprueft |
| pinokio | Pinokio | planned / manual-desktop | scripts/tools/pinokio_install.sh: Skript vorhanden; Runtime ungeprueft |
| sdnext | SD_Next | experimental / source | scripts/tools/sdnext_install.sh: Skript vorhanden; Runtime ungeprueft |
| windmill | Windmill | experimental / source | scripts/tools/windmill_install.sh: Skript vorhanden; Runtime ungeprueft |
| fal_client | Fal_Client | experimental / source | scripts/tools/fal_client_install.sh: Skript vorhanden; Runtime ungeprueft |
| veo_api | Veo_API | experimental / source | scripts/tools/veo_api_install.sh: Skript vorhanden; Runtime ungeprueft |
| hf_datasets | HF_Datasets | experimental / source | scripts/tools/hf_datasets_install.sh: Skript vorhanden; Runtime ungeprueft |
| hf_hub | HF_Hub | experimental / source | scripts/tools/hf_hub_install.sh: Skript vorhanden; Runtime ungeprueft |
| video2dataset | Video2Dataset | experimental / github-source | scripts/tools/video2dataset_install.sh: Skript vorhanden; Runtime ungeprueft |
| karaoke_formats | Karaoke_Formats | experimental / source | scripts/tools/karaoke_formats_install.sh: Skript vorhanden; Runtime ungeprueft |
| alexandria_audiobook | Alexandria_Audiobook | experimental / source | scripts/tools/alexandria_audiobook_install.sh: Skript vorhanden; Runtime ungeprueft |
| qwen3_tts | Qwen3_TTS | experimental / source | scripts/tools/qwen3_tts_install.sh: Skript vorhanden; Runtime ungeprueft |
| chattts | ChatTTS | experimental / source | scripts/tools/chattts_install.sh: Skript vorhanden; Runtime ungeprueft |
| audioldm2 | AudioLDM2 | experimental / source | scripts/tools/audioldm2_install.sh: Skript vorhanden; Runtime ungeprueft |
| audiogen | AudioGen | experimental / source | scripts/tools/audiogen_install.sh: Skript vorhanden; Runtime ungeprueft |
| stable_audio_open | Stable_Audio_Open | experimental / source | scripts/tools/stable_audio_open_install.sh: Skript vorhanden; Runtime ungeprueft |
| moshi | Moshi | experimental / source | scripts/tools/moshi_install.sh: Skript vorhanden; Runtime ungeprueft |
| moss_tts | MOSS_TTS | experimental / source | scripts/tools/moss_tts_install.sh: Skript vorhanden; Runtime ungeprueft |
| yue | YuE | experimental / source | scripts/tools/yue_install.sh: Skript vorhanden; Runtime ungeprueft |
| ace_step_15 | ACE_Step_15 | experimental / source | scripts/tools/ace_step_15_install.sh: Skript vorhanden; Runtime ungeprueft |
| whisperx | WhisperX | experimental / source | scripts/tools/whisperx_install.sh: Skript vorhanden; Runtime ungeprueft |
| aegisub | Aegisub | experimental / source | scripts/tools/aegisub_install.sh: Skript vorhanden; Runtime ungeprueft |
| basic_pitch | Basic_Pitch | experimental / source | scripts/tools/basic_pitch_install.sh: Skript vorhanden; Runtime ungeprueft |
| sfizz | Sfizz | experimental / source | scripts/tools/sfizz_install.sh: Skript vorhanden; Runtime ungeprueft |
| aida_x | AIDA_X | experimental / source | scripts/tools/aida_x_install.sh: Skript vorhanden; Runtime ungeprueft |
| propainter | ProPainter | experimental / source | scripts/tools/propainter_install.sh: Skript vorhanden; Runtime ungeprueft |
| kiwi_edit | Kiwi_Edit | experimental / source | scripts/tools/kiwi_edit_install.sh: Skript vorhanden; Runtime ungeprueft |
| void_model | VOID_Model | experimental / source | scripts/tools/void_model_install.sh: Skript vorhanden; Runtime ungeprueft |
| just_dub_it | Just_Dub_It | experimental / source | scripts/tools/just_dub_it_install.sh: Skript vorhanden; Runtime ungeprueft |
| vidubb | ViDubb | experimental / source | scripts/tools/vidubb_install.sh: Skript vorhanden; Runtime ungeprueft |
| agent_framework | Microsoft_Agent_Framework | experimental / source | scripts/tools/agent_framework_install.sh: Skript vorhanden; Runtime ungeprueft |
| personnel_documents | Personnel_Documents_AI | experimental / source | scripts/tools/personnel_documents_install.sh: Skript vorhanden; Runtime ungeprueft |
| automaton | Automaton | experimental / source | scripts/tools/automaton_install.sh: Skript vorhanden; Runtime ungeprueft |
| embedded_debug_hil | Embedded_Debug_HIL | experimental / source | scripts/tools/embedded_debug_hil_install.sh: Skript vorhanden; Runtime ungeprueft |
| freellmapi | FreeLLMAPI | experimental / source | scripts/tools/freellmapi_install.sh: Skript vorhanden; Runtime ungeprueft |
| rife | RIFE | experimental / venv | scripts/tools/rife_install.sh: Skript vorhanden; Runtime ungeprueft |
| velero | Velero | planned / binary | scripts/tools/velero_install.sh: Skript vorhanden; Runtime ungeprueft |
| k9s | K9s | planned / binary | scripts/tools/k9s_install.sh: Skript vorhanden; Runtime ungeprueft |
| ollama | Ollama | nicht angegeben / nicht angegeben | scripts/tools/ollama_install.sh: Skript vorhanden; Runtime ungeprueft |
| openclaw | OpenClaw | nicht angegeben / nicht angegeben | scripts/tools/openclaw_install.sh: Skript vorhanden; Runtime ungeprueft |
| ruflo | Ruflo | nicht angegeben / nicht angegeben | scripts/tools/ruflo_install.sh: Skript vorhanden; Runtime ungeprueft |
| litellm | LiteLLM | experimental / github-native-build | scripts/tools/litellm_install.sh: Skript vorhanden; Runtime ungeprueft |
| open_webui | Open_WebUI | experimental / github-native-build | scripts/tools/open_webui_install.sh: Skript vorhanden; Runtime ungeprueft |
| qdrant | Qdrant | experimental / github-native-build | scripts/tools/qdrant_install.sh: Skript vorhanden; Runtime ungeprueft |
| chromadb | ChromaDB | nicht angegeben / nicht angegeben | scripts/tools/chromadb_install.sh: Skript vorhanden; Runtime ungeprueft |
| lightrag | nein | nicht angegeben / nicht angegeben | scripts/tools/lightrag_install.sh: Skript vorhanden; Runtime ungeprueft |
| langfuse | Langfuse | experimental / github-native-build | scripts/tools/langfuse_install.sh: Skript vorhanden; Runtime ungeprueft |
| openlit | OpenLIT | nicht angegeben / nicht angegeben | scripts/tools/openlit_install.sh: Skript vorhanden; Runtime ungeprueft |
| prometheus | Prometheus | experimental / github-native-build | scripts/tools/prometheus_install.sh: Skript vorhanden; Runtime ungeprueft |
| grafana | Grafana | experimental / github-native-build | scripts/tools/grafana_install.sh: Skript vorhanden; Runtime ungeprueft |
| loki | Loki | experimental / github-native-build | scripts/tools/loki_install.sh: Skript vorhanden; Runtime ungeprueft |
| uptime_kuma | Uptime_Kuma | experimental / github-native-build | scripts/tools/uptime_kuma_install.sh: Skript vorhanden; Runtime ungeprueft |
| healthchecks | Healthchecks | experimental / github-native-build | scripts/tools/healthchecks_install.sh: Skript vorhanden; Runtime ungeprueft |
| mail_utils_msmtp | Mail_Utils_MSMTP | nicht angegeben / nicht angegeben | scripts/tools/mail_utils_msmtp_install.sh: Skript vorhanden; Runtime ungeprueft |
| trivy | Trivy | nicht angegeben / nicht angegeben | scripts/tools/trivy_install.sh: Skript vorhanden; Runtime ungeprueft |
| gitleaks | Gitleaks | nicht angegeben / nicht angegeben | scripts/tools/gitleaks_install.sh: Skript vorhanden; Runtime ungeprueft |
| semgrep | Semgrep | nicht angegeben / nicht angegeben | scripts/tools/semgrep_install.sh: Skript vorhanden; Runtime ungeprueft |
| crowdsec | CrowdSec | experimental / github-native-build | scripts/tools/crowdsec_install.sh: Skript vorhanden; Runtime ungeprueft |
| ufw | nein | nicht angegeben / nicht angegeben | scripts/tools/ufw_install.sh: Skript vorhanden; Runtime ungeprueft |
| tailscale | nein | nicht angegeben / nicht angegeben | scripts/tools/tailscale_install.sh: Skript vorhanden; Runtime ungeprueft |
| cloudflared | Cloudflared | experimental / source | scripts/tools/cloudflared_install.sh: Skript vorhanden; Runtime ungeprueft |
| authentik | Authentik | nicht angegeben / nicht angegeben | scripts/tools/authentik_install.sh: Skript vorhanden; Runtime ungeprueft |
| authelia | Authelia | nicht angegeben / nicht angegeben | scripts/tools/authelia_install.sh: Skript vorhanden; Runtime ungeprueft |
| node_red | Node_Red | experimental / github-native-build | scripts/tools/node_red_install.sh: Skript vorhanden; Runtime ungeprueft |
| mosquitto | Mosquitto | experimental / github-native-build | scripts/tools/mosquitto_install.sh: Skript vorhanden; Runtime ungeprueft |
| zigbee2mqtt | Zigbee2MQTT | experimental / github-native-build | scripts/tools/zigbee2mqtt_install.sh: Skript vorhanden; Runtime ungeprueft |
| esphome | nein | nicht angegeben / nicht angegeben | scripts/tools/esphome_install.sh: Skript vorhanden; Runtime ungeprueft |
| paperless_ngx | Paperless_NGX | experimental / docker | scripts/tools/paperless_ngx_install.sh: Skript vorhanden; Runtime ungeprueft |
| stirling_pdf | Stirling_PDF | experimental / github-native-build | scripts/tools/stirling_pdf_install.sh: Skript vorhanden; Runtime ungeprueft |
| apache_tika | Apache_Tika | experimental / github-native-build | scripts/tools/apache_tika_install.sh: Skript vorhanden; Runtime ungeprueft |
| docling | Docling | nicht angegeben / nicht angegeben | scripts/tools/docling_install.sh: Skript vorhanden; Runtime ungeprueft |
| pandoc | Pandoc | nicht angegeben / nicht angegeben | scripts/tools/pandoc_install.sh: Skript vorhanden; Runtime ungeprueft |
| jupyterlab | JupyterLab | nicht angegeben / pypi-venv-default-source-optional | scripts/tools/jupyterlab_install.sh: Skript vorhanden; Runtime ungeprueft |
| duckdb | DuckDB | stable / github-release-binary | scripts/tools/duckdb_install.sh: Skript vorhanden; Runtime ungeprueft |
| metabase | Metabase | experimental / github-native-build | scripts/tools/metabase_install.sh: Skript vorhanden; Runtime ungeprueft |
| airbyte | Airbyte | planned / native-migration-blocked | scripts/tools/airbyte_install.sh: Skript vorhanden; Runtime ungeprueft |
| minio | MinIO | experimental / github-native-build | scripts/tools/minio_install.sh: Skript vorhanden; Runtime ungeprueft |
| restic | Restic | nicht angegeben / nicht angegeben | scripts/tools/restic_install.sh: Skript vorhanden; Runtime ungeprueft |
| borgbackup | nein | nicht angegeben / nicht angegeben | scripts/tools/borgbackup_install.sh: Skript vorhanden; Runtime ungeprueft |
| rclone | Rclone | nicht angegeben / nicht angegeben | scripts/tools/rclone_install.sh: Skript vorhanden; Runtime ungeprueft |
| comfyui | ComfyUI | nicht angegeben / nicht angegeben | scripts/tools/comfyui_install.sh: Skript vorhanden; Runtime ungeprueft |
| stable_diffusion_webui_forge | Stable_Diffusion_WebUI_Forge | experimental / nicht angegeben | scripts/tools/stable_diffusion_webui_forge_install.sh: Skript vorhanden; Runtime ungeprueft |
| gfpgan | GFPGAN | nicht angegeben / nicht angegeben | scripts/tools/gfpgan_install.sh: Skript vorhanden; Runtime ungeprueft |
| realesrgan | RealESRGAN | nicht angegeben / nicht angegeben | scripts/tools/realesrgan_install.sh: Skript vorhanden; Runtime ungeprueft |
| rembg | Rembg | nicht angegeben / nicht angegeben | scripts/tools/rembg_install.sh: Skript vorhanden; Runtime ungeprueft |
| whisper_cpp | Whisper_CPP | nicht angegeben / nicht angegeben | scripts/tools/whisper_cpp_install.sh: Skript vorhanden; Runtime ungeprueft |
| faster_whisper | Faster_Whisper | nicht angegeben / nicht angegeben | scripts/tools/faster_whisper_install.sh: Skript vorhanden; Runtime ungeprueft |
| ffmpeg | FFmpeg | experimental / github-native-build | scripts/tools/ffmpeg_install.sh: Skript vorhanden; Runtime ungeprueft |
| piper | Piper | nicht angegeben / nicht angegeben | scripts/tools/piper_install.sh: Skript vorhanden; Runtime ungeprueft |
| coqui_tts | Coqui_TTS | experimental / venv | scripts/tools/coqui_tts_install.sh: Skript vorhanden; Runtime ungeprueft |
| demucs | Demucs | nicht angegeben / nicht angegeben | scripts/tools/demucs_install.sh: Skript vorhanden; Runtime ungeprueft |
| blender | Blender | nicht angegeben / nicht angegeben | scripts/tools/blender_install.sh: Skript vorhanden; Runtime ungeprueft |
| github_cli | GitHub_CLI | nicht angegeben / nicht angegeben | scripts/tools/github_cli_install.sh: Skript vorhanden; Runtime ungeprueft |
| act | Act | nicht angegeben / nicht angegeben | scripts/tools/act_install.sh: Skript vorhanden; Runtime ungeprueft |
| pre_commit | Pre_Commit | nicht angegeben / nicht angegeben | scripts/tools/pre_commit_install.sh: Skript vorhanden; Runtime ungeprueft |
| release_please | Release_Please | nicht angegeben / nicht angegeben | scripts/tools/release_please_install.sh: Skript vorhanden; Runtime ungeprueft |
| changelog_generator | Changelog_Generator | nicht angegeben / nicht angegeben | scripts/tools/changelog_generator_install.sh: Skript vorhanden; Runtime ungeprueft |
| aider | Aider | experimental / source | scripts/tools/aider_install.sh: Skript vorhanden; Runtime ungeprueft |
| openhands | OpenHands | experimental / source | scripts/tools/openhands_install.sh: Skript vorhanden; Runtime ungeprueft |
| continue_dev | Continue_Dev | nicht angegeben / nicht angegeben | scripts/tools/continue_dev_install.sh: Skript vorhanden; Runtime ungeprueft |
| langgraph | LangGraph | nicht angegeben / nicht angegeben | scripts/tools/langgraph_install.sh: Skript vorhanden; Runtime ungeprueft |
| crewai | CrewAI | nicht angegeben / nicht angegeben | scripts/tools/crewai_install.sh: Skript vorhanden; Runtime ungeprueft |
| autogen | AutoGen | nicht angegeben / nicht angegeben | scripts/tools/autogen_install.sh: Skript vorhanden; Runtime ungeprueft |
| playwright | Playwright | nicht angegeben / nicht angegeben | scripts/tools/playwright_install.sh: Skript vorhanden; Runtime ungeprueft |
| puppeteer | Puppeteer | nicht angegeben / nicht angegeben | scripts/tools/puppeteer_install.sh: Skript vorhanden; Runtime ungeprueft |
| flowise | Flowise | optional / git-pnpm | scripts/tools/flowise_install.sh: Skript vorhanden; Runtime ungeprueft |
| langflow | LangFlow | nicht angegeben / nicht angegeben | scripts/tools/langflow_install.sh: Skript vorhanden; Runtime ungeprueft |
| n8n | n8n | nicht angegeben / nicht angegeben | scripts/tools/n8n_install.sh: Skript vorhanden; Runtime ungeprueft |
| activepieces | Activepieces | nicht angegeben / nicht angegeben | scripts/tools/activepieces_install.sh: Skript vorhanden; Runtime ungeprueft |
| appsmith | Appsmith | experimental / github-native-build | scripts/tools/appsmith_install.sh: Skript vorhanden; Runtime ungeprueft |
| budibase | Budibase | experimental / github-native-build | scripts/tools/budibase_install.sh: Skript vorhanden; Runtime ungeprueft |
| nocodb | NocoDB | experimental / github-native-build | scripts/tools/nocodb_install.sh: Skript vorhanden; Runtime ungeprueft |
| directus | Directus | experimental / github-native-build | scripts/tools/directus_install.sh: Skript vorhanden; Runtime ungeprueft |
| home_assistant | Home_Assistant | experimental / github-native-build | scripts/tools/home_assistant_install.sh: Skript vorhanden; Runtime ungeprueft |
| nextcloud | Nextcloud | experimental / github-native-build | scripts/tools/nextcloud_install.sh: Skript vorhanden; Runtime ungeprueft |
| llamaindex | LlamaIndex | nicht angegeben / nicht angegeben | scripts/tools/llamaindex_install.sh: Skript vorhanden; Runtime ungeprueft |
| unstructured | Unstructured | nicht angegeben / nicht angegeben | scripts/tools/unstructured_install.sh: Skript vorhanden; Runtime ungeprueft |
| marker | Marker | nicht angegeben / nicht angegeben | scripts/tools/marker_install.sh: Skript vorhanden; Runtime ungeprueft |
| meilisearch | Meilisearch | experimental / github-native-build | scripts/tools/meilisearch_install.sh: Skript vorhanden; Runtime ungeprueft |
| promptfoo | Promptfoo | experimental / source | scripts/tools/promptfoo_install.sh: Skript vorhanden; Runtime ungeprueft |
| syft | Syft | experimental / binary | scripts/tools/syft_install.sh: Skript vorhanden; Runtime ungeprueft |
| grype | Grype | stable / github-release-binary-checksum | scripts/tools/grype_install.sh: Skript vorhanden; Runtime ungeprueft |
| fail2ban | Fail2Ban | nicht angegeben / nicht angegeben | scripts/tools/fail2ban_install.sh: Skript vorhanden; Runtime ungeprueft |
| opentofu | OpenTofu | nicht angegeben / nicht angegeben | scripts/tools/opentofu_install.sh: Skript vorhanden; Runtime ungeprueft |
| ansible | Ansible | nicht angegeben / nicht angegeben | scripts/tools/ansible_install.sh: Skript vorhanden; Runtime ungeprueft |
| argocd_cli | ArgoCD_CLI | experimental / source | scripts/tools/argocd_cli_install.sh: Skript vorhanden; Runtime ungeprueft |
| grafana_alloy | Grafana_Alloy | experimental / github-native-build | scripts/tools/grafana_alloy_install.sh: Skript vorhanden; Runtime ungeprueft |
| netdata | Netdata | experimental / github-native-build | scripts/tools/netdata_install.sh: Skript vorhanden; Runtime ungeprueft |
| clamav | nein | optional / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| yara | nein | nicht angegeben / nicht angegeben | scripts/tools/yara_install.sh: Skript vorhanden; Runtime ungeprueft |
| searxng | SearXNG | experimental / github-native-build | scripts/tools/searxng_install.sh: Skript vorhanden; Runtime ungeprueft |
| firecrawl | Firecrawl | nicht angegeben / nicht angegeben | scripts/tools/firecrawl_install.sh: Skript vorhanden; Runtime ungeprueft |
| haystack | nein | nicht angegeben / nicht angegeben | scripts/tools/haystack_install.sh: Skript vorhanden; Runtime ungeprueft |
| node_exporter | Node_Exporter | experimental / github-native-build | scripts/tools/node_exporter_install.sh: Skript vorhanden; Runtime ungeprueft |
| cadvisor | cAdvisor | experimental / github-native-build | scripts/tools/cadvisor_install.sh: Skript vorhanden; Runtime ungeprueft |
| postgres | Postgres | nicht angegeben / nicht angegeben | scripts/tools/postgres_install.sh: Skript vorhanden; Runtime ungeprueft |
| redis | Redis | nicht angegeben / nicht angegeben | scripts/tools/redis_install.sh: Skript vorhanden; Runtime ungeprueft |
| huginn | Huginn | nicht angegeben / nicht angegeben | scripts/tools/huginn_install.sh: Skript vorhanden; Runtime ungeprueft |
| forgejo | Forgejo | experimental / github-native-build | scripts/tools/forgejo_install.sh: Skript vorhanden; Runtime ungeprueft |
| penpot | Penpot | experimental / github-native-build | scripts/tools/penpot_install.sh: Skript vorhanden; Runtime ungeprueft |
| tesseract | Tesseract | nicht angegeben / nicht angegeben | scripts/tools/tesseract_install.sh: Skript vorhanden; Runtime ungeprueft |
| syncthing | Syncthing | nicht angegeben / nicht angegeben | scripts/tools/syncthing_install.sh: Skript vorhanden; Runtime ungeprueft |
| pytest | nein | nicht angegeben / nicht angegeben | scripts/tools/pytest_install.sh: Skript vorhanden; Runtime ungeprueft |
| shellcheck | ShellCheck | nicht angegeben / nicht angegeben | scripts/tools/shellcheck_install.sh: Skript vorhanden; Runtime ungeprueft |
| shfmt | Shfmt | nicht angegeben / nicht angegeben | scripts/tools/shfmt_install.sh: Skript vorhanden; Runtime ungeprueft |
| deepeval | nein | nicht angegeben / nicht angegeben | scripts/tools/deepeval_install.sh: Skript vorhanden; Runtime ungeprueft |
| pihole | nein | nicht angegeben / nicht angegeben | scripts/tools/pihole_install.sh: Skript vorhanden; Runtime ungeprueft |
| adguard_home | nein | nicht angegeben / nicht angegeben | scripts/tools/adguard_home_install.sh: Skript vorhanden; Runtime ungeprueft |
| trafilatura | nein | nicht angegeben / nicht angegeben | scripts/tools/trafilatura_install.sh: Skript vorhanden; Runtime ungeprueft |
| reuse | nein | nicht angegeben / nicht angegeben | scripts/tools/reuse_install.sh: Skript vorhanden; Runtime ungeprueft |
| scancode_toolkit | nein | nicht angegeben / nicht angegeben | scripts/tools/scancode_toolkit_install.sh: Skript vorhanden; Runtime ungeprueft |
| gbox | nein | nicht angegeben / nicht angegeben | scripts/tools/gbox_install.sh: Skript vorhanden; Runtime ungeprueft |
| ai_content_multiplier | AI_ContentMultiplier | nicht angegeben / nicht angegeben | scripts/tools/ai_content_multiplier_install.sh: Skript vorhanden; Runtime ungeprueft |
| websitefactory | WebsiteFactory | optional / nicht angegeben | scripts/tools/websitefactory_install.sh: Skript vorhanden; Runtime ungeprueft |
| stalwart_mail | nein | nicht angegeben / nicht angegeben | scripts/tools/stalwart_mail_install.sh: Skript vorhanden; Runtime ungeprueft |
| queue_manager | nein | planned / nicht angegeben | scripts/tools/queue_manager_install.sh: Skript vorhanden; Runtime ungeprueft |
| tasktiger | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| rq | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| celery | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| dramatiq | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| bullmq | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| temporal | Temporal | experimental / github-native-build | scripts/tools/temporal_install.sh: Skript vorhanden; Runtime ungeprueft |
| argo_workflows | Argo_Workflows | experimental / github-native-build | scripts/tools/argo_workflows_install.sh: Skript vorhanden; Runtime ungeprueft |
| guardrails_ai | Guardrails_AI | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| opencode | OpenCode | experimental / source | scripts/tools/opencode_install.sh: Skript vorhanden; Runtime ungeprueft |
| swe_agent | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| cosign | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| sops | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| age | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| vaultwarden | Vaultwarden | experimental / github-native-build | scripts/tools/vaultwarden_install.sh: Skript vorhanden; Runtime ungeprueft |
| suricata | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| wazuh | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| headscale | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| headplane | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| wireguard | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| frp | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| nginx_proxy_manager | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| caddy | Caddy | experimental / github-native-build | scripts/tools/caddy_install.sh: Skript vorhanden; Runtime ungeprueft |
| traefik | Traefik | experimental / github-native-build | scripts/tools/traefik_install.sh: Skript vorhanden; Runtime ungeprueft |
| ddclient_he | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| acme_sh | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| rspamd | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| roundcube | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| snappymail | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| mailpit | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| opendkim | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| opendmarc | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| kopia | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| supabase_self_hosted | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| duplicati | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| invokeai | InvokeAI | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| automatic1111 | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| krita_ai_diffusion | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| job_queue | nein | beta / nicht angegeben | scripts/tools/job_queue_install.sh: Skript vorhanden; Runtime ungeprueft |
| modelcontextprotocol_servers | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| mcp_filesystem | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| mcp_git | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| mcp_github | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| mcp_shell | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| mcp_browser | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| mcp_sqlite | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| mcp_postgres | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| mcp_fetch | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| mcp_memory | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| supervisord | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| systemd_user_units | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| tmux | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| pm2 | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| lynis | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| openscap | nein | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| ocrmypdf | OCRmyPDF | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| zotero | Zotero | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| langchain | LangChain | planned / nicht angegeben | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| autogpt | AutoGPT | planned / native-blocked | scripts/tools/autogpt_install.sh: Skript vorhanden; Runtime ungeprueft |
| supabase | Supabase | planned / native-blocked | scripts/tools/supabase_install.sh: Skript vorhanden; Runtime ungeprueft |
| gitops_bootstrap | GitOps_Bootstrap | experimental / manual | scripts/tools/gitops_bootstrap_install.sh: Skript vorhanden; Runtime ungeprueft |
| kubeseal | Kubeseal | experimental / github-native-build | scripts/tools/kubeseal_install.sh: Skript vorhanden; Runtime ungeprueft |
| opentelemetry | OpenTelemetry | experimental / github-native-build | scripts/tools/opentelemetry_install.sh: Skript vorhanden; Runtime ungeprueft |
| mcp_filesystem_server | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| mcp_git_server | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| mcp_github_server | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| mcp_shell_server | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| mcp_browser_server | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| mcp_sqlite_server | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| mcp_postgres_server | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| mcp_fetch_server | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| mcp_memory_server | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| styletts2 | nein | planned / source | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| openvoice | nein | planned / source | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| rvc | RVC | experimental / github-source | scripts/tools/rvc_install.sh: Skript vorhanden; Runtime ungeprueft |
| seed_vc | nein | experimental / github-source | scripts/tools/seed_vc_install.sh: Skript vorhanden; Runtime ungeprueft |
| diffsinger | nein | experimental / github-source | scripts/tools/diffsinger_install.sh: Skript vorhanden; Runtime ungeprueft |
| openutau | nein | experimental / github-source | scripts/tools/openutau_install.sh: Skript vorhanden; Runtime ungeprueft |
| nnsvs | nein | planned / source | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| audacity | Audacity | experimental / github-source | scripts/tools/audacity_install.sh: Skript vorhanden; Runtime ungeprueft |
| uvr5 | UVR5 | experimental / github-source | scripts/tools/uvr5_install.sh: Skript vorhanden; Runtime ungeprueft |
| fish_speech | nein | planned / source | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| melotts | nein | planned / source | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| kokoro_tts | nein | planned / python | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| spark_tts | nein | planned / source | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| hallo2 | nein | planned / source | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| musetalk | MuseTalk | experimental / github-python-runtime | scripts/tools/musetalk_install.sh: Skript vorhanden; Runtime ungeprueft |
| liveportrait | LivePortrait | experimental / github-source | scripts/tools/liveportrait_install.sh: Skript vorhanden; Runtime ungeprueft |
| sadtalker | SadTalker | experimental / github-source | scripts/tools/sadtalker_install.sh: Skript vorhanden; Runtime ungeprueft |
| emo_avatar | nein | planned / source | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| skyreels_a1 | nein | planned / source | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| wav2lip | nein | planned / source | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| clearer_voice_studio | nein | planned / source | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| obs | OBS | experimental / github-source | scripts/tools/obs_install.sh: Skript vorhanden; Runtime ungeprueft |
| subtitleedit | nein | optional / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| openbao | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| infisical | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| glances | nein | optional / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| blocky | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| llama_cpp | Llama_CPP | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| vllm | vLLM | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| localai | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| browsermcp | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| docker_mcp_registry | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| rabbitmq | RabbitMQ | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| pass | nein | optional / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| litestream | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| fastlane | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| apktool | nein | optional / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| mitmproxy | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| k3s | K3s | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| helm | Helm | optional / official-release-checksum | scripts/tools/helm_install.sh: Skript vorhanden; Runtime ungeprueft |
| mcpo | MCPO | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| nmap | Nmap | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| radicale | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| trufflehog | TruffleHog | experimental / github-native-build | scripts/tools/trufflehog_install.sh: Skript vorhanden; Runtime ungeprueft |
| imap_importer | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| git | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| doctor | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| wsl2 | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| kubectl | Kubectl | planned / binary | scripts/tools/kubectl_install.sh: Skript vorhanden; Runtime ungeprueft |
| neo4j | Neo4j | experimental / github-native-build | scripts/tools/neo4j_install.sh: Skript vorhanden; Runtime ungeprueft |
| musicgen | MusicGen | planned / github-source | scripts/tools/musicgen_source_install.sh: Skript vorhanden; Runtime ungeprueft |
| wyoming | Wyoming | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| openwakeword | openWakeWord | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| voice_studio | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| podcast_studio | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| audiobook_studio | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| dubbing_studio | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| prompt_generator_studio | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| video_ai_production | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| character_library | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| voice_clone | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| ai_choir | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| android_sdk | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| gradle | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| jadx | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| dbt | dbt | optional / git-subdirectory-venv | scripts/tools/dbt_install.sh: Skript vorhanden; Runtime ungeprueft |
| prefect | Prefect | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| arq | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| apscheduler | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| promtail | Promtail | experimental / github-native-build | scripts/tools/promtail_install.sh: Skript vorhanden; Runtime ungeprueft |
| weaviate | Weaviate | experimental / github-native-build | scripts/tools/weaviate_install.sh: Skript vorhanden; Runtime ungeprueft |
| kustomize | Kustomize | planned / binary | scripts/tools/kustomize_install.sh: Skript vorhanden; Runtime ungeprueft |
| renovate | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| check_resource_budget | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| mkdocs | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| podman | Podman | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| docker | Docker | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| firejail | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| wakeonlan | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| nvidia_smi | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| ddclient | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| markdownlint_cli | Markdownlint_CLI | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| check_tools | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| check_profiles | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| check_ports | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| paddleocr | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| livekit | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| asterisk | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| beszel | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| zeek | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| falco | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| stalwart | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| sieve | nein | planned / manual | scripts/tools/planned_tool_stub_install.sh: Platzhalter |
| finrag | FinRAG | optional / git-venv-auto-cpython311-build | scripts/tools/finrag_install.sh: Skript vorhanden; Runtime ungeprueft |
| finrobot | FinRobot | optional / git-venv-auto-cpython311-build | scripts/tools/finrobot_install.sh: Skript vorhanden; Runtime ungeprueft |
| flux_cli | Flux_CLI | optional / github-release-binary-checksum | scripts/tools/flux_cli_install.sh: Skript vorhanden; Runtime ungeprueft |
| archivebox | ArchiveBox | experimental / github-native-build | scripts/tools/archivebox_install.sh: Skript vorhanden; Runtime ungeprueft |
| argilla | Argilla | experimental / github-native-build | scripts/tools/argilla_install.sh: Skript vorhanden; Runtime ungeprueft |
| changedetection_io | Changedetection_IO | experimental / github-native-build | scripts/tools/changedetection_io_install.sh: Skript vorhanden; Runtime ungeprueft |
| rhasspy | Rhasspy | planned / native-migration-blocked | scripts/tools/rhasspy_install.sh: Skript vorhanden; Runtime ungeprueft |
| vault | Vault | experimental / github-native-build | scripts/tools/vault_install.sh: Skript vorhanden; Runtime ungeprueft |
| vikunja | Vikunja | experimental / github-native-build | scripts/tools/vikunja_install.sh: Skript vorhanden; Runtime ungeprueft |
| watchtower | Watchtower | experimental / github-native-build | scripts/tools/watchtower_install.sh: Skript vorhanden; Runtime ungeprueft |
| pyairbyte | PyAirbyte | experimental / github-native-build | scripts/tools/pyairbyte_install.sh: Skript vorhanden; Runtime ungeprueft |
| xerj | XERJ | experimental / github-native-build | scripts/tools/xerj_install.sh: Skript vorhanden; Runtime ungeprueft |
| markdown_docs_server | Markdown_Docs_Server | experimental / github-native-build | scripts/tools/markdown_docs_server_install.sh: Skript vorhanden; Runtime ungeprueft |
| openjarvis | OpenJarvis | experimental / github-native-build | scripts/tools/openjarvis_install.sh: Skript vorhanden; Runtime ungeprueft |

## Separater Entwicklungskatalog

Nur Rezept-/Dateizuordnung, keine Build-Abnahme. workflow-package aktiviert keine CI und editor-package keinen Editor.

| Quelle | ID | Rezeptmodus | Dateiverweise |
|---|---|---|---|
| Node.js | node_js | native-build | keine fehlenden Adapter-Dateien |
| TypeScript | typescript | node-package | keine fehlenden Adapter-Dateien |
| Prettier | prettier | node-package | keine fehlenden Adapter-Dateien |
| ESLint | eslint | node-package | keine fehlenden Adapter-Dateien |
| Vitest | vitest | node-package | keine fehlenden Adapter-Dateien |
| Vite | vite | node-package | keine fehlenden Adapter-Dateien |
| Playwright | playwright | node-package | keine fehlenden Adapter-Dateien |
| pnpm | pnpm | node-package | keine fehlenden Adapter-Dateien |
| Go | go | toolchain-build | keine fehlenden Adapter-Dateien |
| golang/tools | golang_tools | existing | keine fehlenden Adapter-Dateien |
| Delve | delve | existing | keine fehlenden Adapter-Dateien |
| golangci-lint | golangci_lint | existing | keine fehlenden Adapter-Dateien |
| Actions Checkout | actions_checkout | workflow-package | keine fehlenden Adapter-Dateien |
| Actions Setup Go | actions_setup_go | workflow-package | keine fehlenden Adapter-Dateien |
| GCC GitHub-Mirror | gcc_github_mirror | native-build | keine fehlenden Adapter-Dateien |
| LLVM | llvm | native-build | keine fehlenden Adapter-Dateien |
| CMake | cmake | native-build | keine fehlenden Adapter-Dateien |
| GoogleTest | googletest | native-build | keine fehlenden Adapter-Dateien |
| Catch2 | catch2 | native-build | keine fehlenden Adapter-Dateien |
| rustup | rustup | cargo-build | keine fehlenden Adapter-Dateien |
| Cargo | cargo | cargo-build | keine fehlenden Adapter-Dateien |
| rustfmt | rustfmt | cargo-build | keine fehlenden Adapter-Dateien |
| Clippy | clippy | cargo-build | keine fehlenden Adapter-Dateien |
| rust-analyzer | rust_analyzer | cargo-build | keine fehlenden Adapter-Dateien |
| ShellCheck | shellcheck | haskell-build | keine fehlenden Adapter-Dateien |
| shfmt | shfmt | go-build | keine fehlenden Adapter-Dateien |
| Bats-core | bats_core | existing | keine fehlenden Adapter-Dateien |
| BashDB | bashdb | native-build | keine fehlenden Adapter-Dateien |
| PowerShell | powershell | powershell-build | keine fehlenden Adapter-Dateien |
| VS-Code-PowerShell | vs_code_powershell | editor-package | keine fehlenden Adapter-Dateien |
| PSScriptAnalyzer | psscriptanalyzer | powershell-module | keine fehlenden Adapter-Dateien |
| Pester | pester | powershell-module | keine fehlenden Adapter-Dateien |
| Invoke-Build | invoke_build | existing | keine fehlenden Adapter-Dateien |
| PostgreSQL GitHub-Mirror | postgres | native-build | keine fehlenden Adapter-Dateien |
| Flyway | flyway | java-package | keine fehlenden Adapter-Dateien |
| SQLFluff | sqlfluff | existing | keine fehlenden Adapter-Dateien |
| dbt Core | dbt | python-package | keine fehlenden Adapter-Dateien |
| pgTAP | pgtap | postgres-extension-package | keine fehlenden Adapter-Dateien |
| Docker CLI | docker_cli | go-build | keine fehlenden Adapter-Dateien |
| Compose | compose | go-build | keine fehlenden Adapter-Dateien |
| Buildx | buildx | go-build | keine fehlenden Adapter-Dateien |
| BuildKit | buildkit | go-build | keine fehlenden Adapter-Dateien |
| Hadolint | hadolint | haskell-build | keine fehlenden Adapter-Dateien |
| Setup Buildx Action | setup_buildx_action | workflow-package | keine fehlenden Adapter-Dateien |
| Build Push Action | build_push_action | workflow-package | keine fehlenden Adapter-Dateien |
| Login Action | login_action | workflow-package | keine fehlenden Adapter-Dateien |
| kubectl | kubectl | native-build | keine fehlenden Adapter-Dateien |
| kind | kind | go-build | keine fehlenden Adapter-Dateien |
| Helm | helm | go-build | keine fehlenden Adapter-Dateien |
| Kustomize | kustomize | go-build | keine fehlenden Adapter-Dateien |
| Kubeconform | kubeconform | existing | keine fehlenden Adapter-Dateien |
| KubeLinter | kubelinter | existing | keine fehlenden Adapter-Dateien |
| Skaffold | skaffold | go-build | keine fehlenden Adapter-Dateien |
| Argo CD | argocd_cli | go-build | keine fehlenden Adapter-Dateien |
| Flux | flux_cli | go-build | keine fehlenden Adapter-Dateien |
| Terraform | terraform | go-build | keine fehlenden Adapter-Dateien |
| Terraform Language Server | terraform_language_server | go-build | keine fehlenden Adapter-Dateien |
| TFLint | tflint | existing | keine fehlenden Adapter-Dateien |
| Checkov | checkov | python-package | keine fehlenden Adapter-Dateien |
| terraform-docs | terraform_docs | existing | keine fehlenden Adapter-Dateien |
| Terratest | terratest | go-library | keine fehlenden Adapter-Dateien |
| Setup Terraform Action | setup_terraform_action | workflow-package | keine fehlenden Adapter-Dateien |

## Dokumentierte GitHub-Quellen

Vollstaendige Liste der erkannten Repository-URLs. Bis zu drei Fundstellen pro Quelle;
mit --format json sind alle Fundstellen verfuegbar. Leere Zuordnung ist keine Installationszusage.

| Quelle | Zuordnung | Dokumentationsfundstellen |
|---|---|---|
| [0xerr0r/blocky](https://github.com/0xerr0r/blocky) | Registry: blocky | [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/blocky.md](tools/registry/blocky.md) |
| [2noise/chattts](https://github.com/2noise/chattts) | Registry: chattts | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_VIDEO_TOOL_CATALOG.md](media_studio/AUDIO_VIDEO_TOOL_CATALOG.md), [docs/tools/chattts.md](tools/chattts.md) |
| [aboutcode-org/scancode-toolkit](https://github.com/aboutcode-org/scancode-toolkit) | Keine direkte Zuordnung; manuell pruefen | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md) |
| [ace-step/ace-step-1.5](https://github.com/ace-step/ace-step-1.5) | Registry: ace_step_15 | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_VIDEO_TOOL_CATALOG.md](media_studio/AUDIO_VIDEO_TOOL_CATALOG.md) |
| [acly/krita-ai-diffusion](https://github.com/acly/krita-ai-diffusion) | Registry: krita_ai_diffusion | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/krita_ai_diffusion.md](tools/registry/krita_ai_diffusion.md) |
| [acmesh-official/acme.sh](https://github.com/acmesh-official/acme.sh) | Registry: acme_sh | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/acme_sh.md](tools/registry/acme_sh.md) |
| [actions/cache](https://github.com/actions/cache) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [actions/checkout](https://github.com/actions/checkout) | 62er-Katalog: actions_checkout | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/manus-development-sources.md](tutorials/manus-development-sources.md) |
| [actions/runner](https://github.com/actions/runner) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/manus-development-sources.md](tutorials/manus-development-sources.md) |
| [actions/runner-images](https://github.com/actions/runner-images) | Keine direkte Zuordnung; manuell pruefen | [docs/agents/CI_REPAIR_STATUS.md](agents/CI_REPAIR_STATUS.md) |
| [actions/setup-go](https://github.com/actions/setup-go) | 62er-Katalog: actions_setup_go | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [actions/upload-artifact](https://github.com/actions/upload-artifact) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [activepieces/activepieces](https://github.com/activepieces/activepieces) | Menue: Activepieces; Registry: activepieces | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/SOCIAL_AVATAR_AUTOMATION.md](media_studio/SOCIAL_AVATAR_AUTOMATION.md) |
| [adam-cad/cadam](https://github.com/adam-cad/cadam) | Keine direkte Zuordnung; manuell pruefen | [docs/Profile/CAD_Konstrukteur.md](Profile/CAD_Konstrukteur.md) |
| [adguardteam/adguardhome](https://github.com/adguardteam/adguardhome) | Keine direkte Zuordnung; manuell pruefen | [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/TOOL_INDEX.md](TOOL_INDEX.md) |
| [adrienverge/yamllint](https://github.com/adrienverge/yamllint) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/claude-development-tooling.md](tutorials/claude-development-tooling.md) |
| [agronholm/anyio](https://github.com/agronholm/anyio) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/grok-development-tooling.md](tutorials/grok-development-tooling.md) |
| [agronholm/apscheduler](https://github.com/agronholm/apscheduler) | Registry: apscheduler | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/apscheduler.md](tools/registry/apscheduler.md) |
| [ai4finance-foundation/fingpt](https://github.com/ai4finance-foundation/fingpt) | Menue: FinGPT | [docs/CUSTOM_SOURCES_AND_BUILDS.md](CUSTOM_SOURCES_AND_BUILDS.md) |
| [ai4finance-foundation/finrag](https://github.com/ai4finance-foundation/finrag) | Menue: FinRAG; Registry: finrag | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/finrag.md](tools/registry/finrag.md) |
| [ai4finance-foundation/finrobot](https://github.com/ai4finance-foundation/finrobot) | Menue: FinRobot; Registry: finrobot | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/finrobot.md](tools/registry/finrobot.md) |
| [aidadsp/aida-x](https://github.com/aidadsp/aida-x) | Registry: aida_x | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_VIDEO_TOOL_CATALOG.md](media_studio/AUDIO_VIDEO_TOOL_CATALOG.md) |
| [aider-ai/aider](https://github.com/aider-ai/aider) | Menue: Aider; Registry: aider | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md) |
| [airbytehq/abctl](https://github.com/airbytehq/abctl) | Keine direkte Zuordnung; manuell pruefen | [docs/AIRBYTE_ABCTL_KUBERNETES_NOTES.md](AIRBYTE_ABCTL_KUBERNETES_NOTES.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md) |
| [airbytehq/airbyte](https://github.com/airbytehq/airbyte) | Menue: Airbyte; Registry: airbyte | [docs/AIRBYTE_ABCTL_KUBERNETES_NOTES.md](AIRBYTE_ABCTL_KUBERNETES_NOTES.md), [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md) |
| [airbytehq/pyairbyte](https://github.com/airbytehq/pyairbyte) | Registry: pyairbyte | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [aitorormazabal/poetry_generation](https://github.com/aitorormazabal/poetry_generation) | Menue: PoeLM; Registry: poelm | [docs/MUSIC_LYRICS_MODEL_CATALOG.md](MUSIC_LYRICS_MODEL_CATALOG.md), [docs/tools/poelm.md](tools/poelm.md) |
| [all-hands-ai/openhands](https://github.com/all-hands-ai/openhands) | Keine direkte Zuordnung; manuell pruefen | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md) |
| [anchore/grype](https://github.com/anchore/grype) | Menue: Grype; Registry: grype | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/GRYPE_INSTALLATION_NOTES.md](GRYPE_INSTALLATION_NOTES.md) |
| [anchore/syft](https://github.com/anchore/syft) | Menue: Syft; Registry: syft | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/REVIEW-2026-11-11.md](REVIEW-2026-11-11.md) |
| [anil-matcha/open-generative-ai](https://github.com/anil-matcha/open-generative-ai) | Keine direkte Zuordnung; manuell pruefen | [docs/Profile/OpenHiggsStack_AI_Cinema_Studio.md](Profile/OpenHiggsStack_AI_Cinema_Studio.md) |
| [anjok07/ultimatevocalremovergui](https://github.com/anjok07/ultimatevocalremovergui) | Menue: UVR5; Registry: uvr5 | [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_DEEPFAKE_REVIEW.md](media_studio/AUDIO_DEEPFAKE_REVIEW.md) |
| [anomalyco/opencode](https://github.com/anomalyco/opencode) | Menue: OpenCode; Registry: opencode | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/agents/CODING_AGENT_INVENTORY.md](agents/CODING_AGENT_INVENTORY.md), [docs/agents/NATIVE_CLI_BUILDS.md](agents/NATIVE_CLI_BUILDS.md) |
| [anthropics/anthropic-cli](https://github.com/anthropics/anthropic-cli) | Registry: anthropic_cli | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/_API-Keys/reviews/2026-10-26.md](_API-Keys/reviews/2026-10-26.md) |
| [anthropics/claude-code](https://github.com/anthropics/claude-code) | Registry: claude_code | [docs/_API-Keys/reviews/2026-10-21.md](_API-Keys/reviews/2026-10-21.md), [docs/_API-Keys/reviews/2026-10-26.md](_API-Keys/reviews/2026-10-26.md), [docs/_API-Keys/reviews/2026-11-02.md](_API-Keys/reviews/2026-11-02.md) |
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [anthropics/skills](https://github.com/anthropics/skills) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [apache/tika](https://github.com/apache/tika) | Menue: Apache_Tika; Registry: apache_tika | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md) |
| [appsmithorg/appsmith](https://github.com/appsmithorg/appsmith) | Menue: Appsmith; Registry: appsmith | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [aquasecurity/kube-bench](https://github.com/aquasecurity/kube-bench) | Menue: Kube_Bench; Registry: kube_bench | [docs/MAINTENANCE_REVIEW_2026-11-10.md](MAINTENANCE_REVIEW_2026-11-10.md), [docs/tools/kube-bench.md](tools/kube-bench.md) |
| [aquasecurity/trivy](https://github.com/aquasecurity/trivy) | Registry: trivy | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/MISSING_TOOLS.md](audit/MISSING_TOOLS.md) |
| [aquasecurity/trivy-operator](https://github.com/aquasecurity/trivy-operator) | Keine direkte Zuordnung; manuell pruefen | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| [archivebox/archivebox](https://github.com/archivebox/archivebox) | Menue: ArchiveBox; Registry: archivebox | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/archivebox.md](tools/archivebox.md) |
| [ardour/ardour](https://github.com/ardour/ardour) | Keine direkte Zuordnung; manuell pruefen | [docs/models/WAN22_AUDIO_MIDI_TOOLCHAIN.md](models/WAN22_AUDIO_MIDI_TOOLCHAIN.md) |
| [argilla-io/argilla](https://github.com/argilla-io/argilla) | Menue: Argilla; Registry: argilla | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [argoproj/argo-cd](https://github.com/argoproj/argo-cd) | 62er-Katalog: argocd_cli; Registry: argocd_cli | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| [argoproj/argo-workflows](https://github.com/argoproj/argo-workflows) | Registry: argo_workflows | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/native-go-controllers.md](tools/native-go-controllers.md), [docs/tools/queue/README.md](tools/queue/README.md) |
| [arize-ai/phoenix](https://github.com/arize-ai/phoenix) | Registry: phoenix | [docs/reviews/2026-10-26-platform-patch-plan.md](reviews/2026-10-26-platform-patch-plan.md), [docs/tools/python-reviewed-native.md](tools/python-reviewed-native.md) |
| [asg017/sqlite-vss](https://github.com/asg017/sqlite-vss) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/qwen-development-tooling.md](tutorials/qwen-development-tooling.md) |
| [asterisk/asterisk](https://github.com/asterisk/asterisk) | Registry: asterisk | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/asterisk.md](tools/registry/asterisk.md) |
| [astral-sh/python-build-standalone](https://github.com/astral-sh/python-build-standalone) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/archivebox.md](tools/archivebox.md) |
| [astral-sh/ruff](https://github.com/astral-sh/ruff) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/claude-development-tooling.md](tutorials/claude-development-tooling.md), [docs/tutorials/grok-development-tooling.md](tutorials/grok-development-tooling.md) |
| [astral-sh/ruff-action](https://github.com/astral-sh/ruff-action) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/manus-development-sources.md](tutorials/manus-development-sources.md) |
| [astral-sh/uv](https://github.com/astral-sh/uv) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/archivebox.md](tools/archivebox.md), [docs/tools/browser_use.md](tools/browser_use.md), [docs/tools/changedetection_io.md](tools/changedetection_io.md) |
| [asvspoof-challenge/asvspoof5](https://github.com/asvspoof-challenge/asvspoof5) | Keine direkte Zuordnung; manuell pruefen | [docs/media_studio/AUDIO_DEEPFAKE_REVIEW.md](media_studio/AUDIO_DEEPFAKE_REVIEW.md) |
| [audacity/audacity](https://github.com/audacity/audacity) | Menue: Audacity; Registry: audacity | [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_DEEPFAKE_REVIEW.md](media_studio/AUDIO_DEEPFAKE_REVIEW.md) |
| [audileteam/audile](https://github.com/audileteam/audile) | Menue: Audile; Registry: audile | [docs/AUDIO_RECOGNITION_AND_DOMAIN_MODELS.md](AUDIO_RECOGNITION_AND_DOMAIN_MODELS.md), [docs/tools/audile.md](tools/audile.md) |
| [authelia/authelia](https://github.com/authelia/authelia) | Keine direkte Zuordnung; manuell pruefen | [docs/AUTH_OIDC_HELM_SECRETS_GUIDE.md](AUTH_OIDC_HELM_SECRETS_GUIDE.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md) |
| [automatic1111/stable-diffusion-webui](https://github.com/automatic1111/stable-diffusion-webui) | Menue: Stable_Diffusion_WebUI; Registry: automatic1111 | [docs/Profil/Interior_RoomGPT_Designer.md](Profil/Interior_RoomGPT_Designer.md), [docs/STABLE_DIFFUSION_WEBUI_INSTALLATION_NOTES.md](STABLE_DIFFUSION_WEBUI_INSTALLATION_NOTES.md), [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md) |
| [axllent/mailpit](https://github.com/axllent/mailpit) | Registry: mailpit | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/mailpit.md](tools/registry/mailpit.md) |
| [axolotl-ai-cloud/axolotl](https://github.com/axolotl-ai-cloud/axolotl) | Menue: Axolotl | [docs/Profil/LLM-Builder.doc.md](Profil/LLM-Builder.doc.md) |
| [babelcloud/gbox](https://github.com/babelcloud/gbox) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/gbox.md](tools/gbox.md) |
| [backstage/backstage](https://github.com/backstage/backstage) | Keine direkte Zuordnung; manuell pruefen | [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md) |
| [bats-core/bats-core](https://github.com/bats-core/bats-core) | 62er-Katalog: bats_core; Registry: bats_core | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/PRODUCTION_BASELINE_CODE.md](PRODUCTION_BASELINE_CODE.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [bazelbuild/bazel](https://github.com/bazelbuild/bazel) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/perplexity-sdk-build.md](tools/perplexity-sdk-build.md), [docs/tools/sandbox-native-candidates.md](tools/sandbox-native-candidates.md), [docs/tools/sandbox-runtimes.md](tools/sandbox-runtimes.md) |
| [benbjohnson/litestream](https://github.com/benbjohnson/litestream) | Registry: litestream | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/litestream.md](tools/registry/litestream.md) |
| [berriai/litellm](https://github.com/berriai/litellm) | Menue: LiteLLM; Registry: litellm | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/PRODUCTION_BASELINE.md](PRODUCTION_BASELINE.md) |
| [bheisler/criterion.rs](https://github.com/bheisler/criterion.rs) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [bigskysoftware/htmx](https://github.com/bigskysoftware/htmx) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [biomejs/biome](https://github.com/biomejs/biome) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [biomejs/setup-biome](https://github.com/biomejs/setup-biome) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [bitnami-labs/sealed-secrets](https://github.com/bitnami-labs/sealed-secrets) | Keine direkte Zuordnung; manuell pruefen | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| [bitnami/sealed-secrets](https://github.com/bitnami/sealed-secrets) | Menue: Kubeseal; Registry: kubeseal | [docs/GITOPS_SMALL_VPS.md](GITOPS_SMALL_VPS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/kubeseal.md](tools/kubeseal.md) |
| [blender/blender](https://github.com/blender/blender) | Menue: Blender; Registry: blender | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/Profile/CAD_Konstrukteur.md](Profile/CAD_Konstrukteur.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [bminor/bash](https://github.com/bminor/bash) | Keine direkte Zuordnung; manuell pruefen | [docs/quality/EXTERNAL_LINK_POLICY.md](quality/EXTERNAL_LINK_POLICY.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [bogdanp/dramatiq](https://github.com/bogdanp/dramatiq) | Registry: dramatiq | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/queue/README.md](tools/queue/README.md), [docs/tools/registry/dramatiq.md](tools/registry/dramatiq.md) |
| [borgbackup/borg](https://github.com/borgbackup/borg) | Registry: borgbackup | [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/borgbackup.md](tools/registry/borgbackup.md) |
| [breakfastquay/rubberband](https://github.com/breakfastquay/rubberband) | Keine direkte Zuordnung; manuell pruefen | [docs/models/WAN22_AUDIO_MIDI_TOOLCHAIN.md](models/WAN22_AUDIO_MIDI_TOOLCHAIN.md) |
| [bridgecrewio/checkov](https://github.com/bridgecrewio/checkov) | 62er-Katalog: checkov; Registry: checkov | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/audit/MISSING_TOOLS.md](audit/MISSING_TOOLS.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md) |
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | Menue: Browser_Use; Registry: browser_use | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/browser_use.md](tools/browser_use.md), [docs/tools/comet-and-browser-research.md](tools/comet-and-browser-research.md) |
| [browserless/browserless](https://github.com/browserless/browserless) | Keine direkte Zuordnung; manuell pruefen | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md) |
| [browsermcp/mcp](https://github.com/browsermcp/mcp) | Registry: browsermcp | [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/browsermcp.md](tools/registry/browsermcp.md) |
| [browseros-ai/browseros](https://github.com/browseros-ai/browseros) | Menue: BrowserOS; Menue: BrowserOS_Study; Registry: browseros; Registry: browseros_study | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/browseros-study.md](tools/browseros-study.md), [docs/tools/comet-and-browser-research.md](tools/comet-and-browser-research.md) |
| [budibase/budibase](https://github.com/budibase/budibase) | Menue: Budibase; Registry: budibase | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [bwendell/gemini-desktop](https://github.com/bwendell/gemini-desktop) | Menue: Gemini_Desktop_Bwendell; Menue: Gemini_Desktop_Bwendell_Source; Registry: gemini_desktop_bwendell; Registry: gemini_desktop_bwendell_source | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/gemini-desktop-clients.md](tools/gemini-desktop-clients.md) |
| [caddyserver/caddy](https://github.com/caddyserver/caddy) | Menue: Caddy; Registry: caddy | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md) |
| [cadquery/cadquery](https://github.com/cadquery/cadquery) | Keine direkte Zuordnung; manuell pruefen | [docs/Profile/CAD_Konstrukteur.md](Profile/CAD_Konstrukteur.md) |
| [calesthio/openmontage](https://github.com/calesthio/openmontage) | Menue: OpenMontage; Registry: openmontage | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/openmontage.md](tools/openmontage.md) |
| [calf-studio-gear/calf](https://github.com/calf-studio-gear/calf) | Keine direkte Zuordnung; manuell pruefen | [docs/models/WAN22_AUDIO_MIDI_TOOLCHAIN.md](models/WAN22_AUDIO_MIDI_TOOLCHAIN.md) |
| [canonical/microk8s](https://github.com/canonical/microk8s) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [canonical/ufw](https://github.com/canonical/ufw) | Registry: ufw | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/quality/EXTERNAL_LINK_POLICY.md](quality/EXTERNAL_LINK_POLICY.md), [docs/tools/registry/ufw.md](tools/registry/ufw.md) |
| [catchorg/catch2](https://github.com/catchorg/catch2) | 62er-Katalog: catch2 | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [celery/celery](https://github.com/celery/celery) | Registry: celery | [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [cert-manager/cert-manager](https://github.com/cert-manager/cert-manager) | Registry: cert_manager | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md), [docs/tools/native-go-controllers.md](tools/native-go-controllers.md) |
| [cheahjs/free-llm-api-resources](https://github.com/cheahjs/free-llm-api-resources) | Keine direkte Zuordnung; manuell pruefen | [docs/_API-Keys/FREE_TIERS_AND_TRIAL_CREDITS.md](_API-Keys/FREE_TIERS_AND_TRIAL_CREDITS.md), [docs/_API-Keys/reviews/2026-10-21.md](_API-Keys/reviews/2026-10-21.md), [docs/_API-Keys/reviews/2026-10-26.md](_API-Keys/reviews/2026-10-26.md) |
| [chroma-core/chroma](https://github.com/chroma-core/chroma) | Registry: chromadb | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [cilium/cilium](https://github.com/cilium/cilium) | Keine direkte Zuordnung; manuell pruefen | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| [cilium/tetragon](https://github.com/cilium/tetragon) | Keine direkte Zuordnung; manuell pruefen | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| [cisco-talos/clamav](https://github.com/cisco-talos/clamav) | Registry: clamav | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/clamav.md](tools/registry/clamav.md) |
| [cisofy/lynis](https://github.com/cisofy/lynis) | Registry: lynis | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/lynis.md](tools/registry/lynis.md) |
| [city96/comfyui-gguf](https://github.com/city96/comfyui-gguf) | Registry: comfyui_gguf | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/HYBRID_MODELS_AND_WAN.md](media_studio/HYBRID_MODELS_AND_WAN.md), [docs/tools/comfyui-gguf.md](tools/comfyui-gguf.md) |
| [clap-rs/clap](https://github.com/clap-rs/clap) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [cli/cli](https://github.com/cli/cli) | Menue: GitHub_CLI | [docs/SETUP_MEMORY.md](SETUP_MEMORY.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/manus-development-sources.md](tutorials/manus-development-sources.md) |
| [cline/cline](https://github.com/cline/cline) | Registry: cline | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/HYBRID_MODELS_AND_WAN.md](media_studio/HYBRID_MODELS_AND_WAN.md), [docs/tools/cline.md](tools/cline.md) |
| [closeio/tasktiger](https://github.com/closeio/tasktiger) | Registry: tasktiger | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/tasktiger.md](tools/registry/tasktiger.md) |
| [cloudflare/cloudflared](https://github.com/cloudflare/cloudflared) | Registry: cloudflared | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [coleam00/local-ai-packaged](https://github.com/coleam00/local-ai-packaged) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [colinhacks/zod](https://github.com/colinhacks/zod) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [comfy-org/comfyui](https://github.com/comfy-org/comfyui) | Keine direkte Zuordnung; manuell pruefen | [docs/Profile/OpenHiggsStack_AI_Cinema_Studio.md](Profile/OpenHiggsStack_AI_Cinema_Studio.md), [docs/Profile/Video_Generation_ComfyUI_Wan.md](Profile/Video_Generation_ComfyUI_Wan.md), [docs/media_studio/EDITABLE_VIDEO_WORKFLOWS.md](media_studio/EDITABLE_VIDEO_WORKFLOWS.md) |
| [comfyanonymous/comfyui](https://github.com/comfyanonymous/comfyui) | Menue: ComfyUI; Registry: comfyui | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/comfyui.md](tools/registry/comfyui.md) |
| [confident-ai/deepeval](https://github.com/confident-ai/deepeval) | Keine direkte Zuordnung; manuell pruefen | [docs/audit/MISSING_TOOLS.md](audit/MISSING_TOOLS.md) |
| [containers/podman](https://github.com/containers/podman) | Registry: podman | [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [containrrr/watchtower](https://github.com/containrrr/watchtower) | Menue: Watchtower; Registry: watchtower | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/watchtower.md](tools/watchtower.md) |
| [continuedev/continue](https://github.com/continuedev/continue) | Menue: Continue_Dev; Registry: continue_dev | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md) |
| [conway-research/automaton](https://github.com/conway-research/automaton) | Registry: automaton | [docs/AGENTIC_CODING_GUIDE.md](AGENTIC_CODING_GUIDE.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/_API-Keys/PROVIDER_KEY_CATALOG.md](_API-Keys/PROVIDER_KEY_CATALOG.md) |
| [coqui-ai/tts](https://github.com/coqui-ai/tts) | Registry: coqui_tts | [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md), [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [coveragepy/coveragepy](https://github.com/coveragepy/coveragepy) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/manus-development-sources.md](tutorials/manus-development-sources.md) |
| [cpp-best-practices/cmake_template](https://github.com/cpp-best-practices/cmake_template) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/qwen-development-tooling.md](tutorials/qwen-development-tooling.md) |
| [cpp-best-practices/cppbestpractices](https://github.com/cpp-best-practices/cppbestpractices) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/qwen-development-tooling.md](tutorials/qwen-development-tooling.md) |
| [crewaiinc/crewai](https://github.com/crewaiinc/crewai) | Registry: crewai | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/audit/MULTI_AGENT_AUDIT_2026-11-05.md](audit/MULTI_AGENT_AUDIT_2026-11-05.md) |
| [crowdsecurity/crowdsec](https://github.com/crowdsecurity/crowdsec) | Menue: CrowdSec; Registry: crowdsec | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md) |
| [cs01/pygdbmi](https://github.com/cs01/pygdbmi) | Registry: embedded_debug_hil | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/embedded-debug-hil.md](tools/embedded-debug-hil.md) |
| [dani-garcia/bw_web_builds](https://github.com/dani-garcia/bw_web_builds) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/security-data-native.md](tools/security-data-native.md) |
| [dani-garcia/vaultwarden](https://github.com/dani-garcia/vaultwarden) | Registry: vaultwarden | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/vaultwarden.md](tools/registry/vaultwarden.md), [docs/tools/security-data-native.md](tools/security-data-native.md) |
| [danielgatis/rembg](https://github.com/danielgatis/rembg) | Menue: Rembg; Registry: rembg | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/rembg.md](tools/registry/rembg.md) |
| [danilogiles/enki-browser](https://github.com/danilogiles/enki-browser) | Menue: Enki_Browser; Menue: Enki_Browser_Study; Registry: enki_browser; Registry: enki_browser_study | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/comet-and-browser-research.md](tools/comet-and-browser-research.md), [docs/tools/enki-browser-study.md](tools/enki-browser-study.md) |
| [data-privacy-stack/presidio](https://github.com/data-privacy-stack/presidio) | Keine direkte Zuordnung; manuell pruefen | [docs/legal/RAG_COMPLIANCE_ARCHITECTURE.md](legal/RAG_COMPLIANCE_ARCHITECTURE.md) |
| [davebben/esp32-llm](https://github.com/davebben/esp32-llm) | Keine direkte Zuordnung; manuell pruefen | [docs/research/ESP32_AI_LINUX_AND_OLLAMA.md](research/ESP32_AI_LINUX_AND_OLLAMA.md) |
| [dbt-labs/dbt](https://github.com/dbt-labs/dbt) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/manus-language-infrastructure-sources.md](tutorials/manus-language-infrastructure-sources.md) |
| [dbt-labs/dbt-core](https://github.com/dbt-labs/dbt-core) | 62er-Katalog: dbt; Menue: dbt; Registry: dbt | [docs/DBT_INSTALLATION_NOTES.md](DBT_INSTALLATION_NOTES.md), [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/TOOL_MATRIX.md](TOOL_MATRIX.md) |
| [ddclient/ddclient](https://github.com/ddclient/ddclient) | Registry: ddclient; Registry: ddclient_he | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/ddclient.md](tools/registry/ddclient.md), [docs/tools/registry/ddclient_he.md](tools/registry/ddclient_he.md) |
| [deepinsight/insightface](https://github.com/deepinsight/insightface) | Keine direkte Zuordnung; manuell pruefen | [docs/media_studio/EDITABLE_VIDEO_WORKFLOWS.md](media_studio/EDITABLE_VIDEO_WORKFLOWS.md) |
| [deepseek-ai/deepseek-r1](https://github.com/deepseek-ai/deepseek-r1) | Menue: DeepSeek_R1; Registry: deepseek_r1 | [docs/AUDIO_RECOGNITION_AND_DOMAIN_MODELS.md](AUDIO_RECOGNITION_AND_DOMAIN_MODELS.md), [docs/media_studio/HYBRID_MODELS_AND_WAN.md](media_studio/HYBRID_MODELS_AND_WAN.md), [docs/models/README.md](models/README.md) |
| [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | Keine direkte Zuordnung; manuell pruefen | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md) |
| [deepspeedai/deepspeed](https://github.com/deepspeedai/deepspeed) | Registry: deepspeed | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [deinname/fingpt](https://github.com/deinname/fingpt) | Keine direkte Zuordnung; manuell pruefen | [docs/CUSTOM_SOURCES_AND_BUILDS.md](CUSTOM_SOURCES_AND_BUILDS.md), [docs/quality/EXTERNAL_LINK_POLICY.md](quality/EXTERNAL_LINK_POLICY.md) |
| [denoland/deno](https://github.com/denoland/deno) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [derailed/k9s](https://github.com/derailed/k9s) | Menue: K9s; Registry: k9s | [docs/K9S_INSTALLATION_NOTES.md](K9S_INSTALLATION_NOTES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [devanasolver/awesome-free-llm-apis](https://github.com/devanasolver/awesome-free-llm-apis) | Keine direkte Zuordnung; manuell pruefen | [docs/_API-Keys/FREE_TIERS_AND_TRIAL_CREDITS.md](_API-Keys/FREE_TIERS_AND_TRIAL_CREDITS.md), [docs/_API-Keys/reviews/2026-10-21.md](_API-Keys/reviews/2026-10-21.md), [docs/_API-Keys/reviews/2026-10-26.md](_API-Keys/reviews/2026-10-26.md) |
| [dgtlmoon/changedetection.io](https://github.com/dgtlmoon/changedetection.io) | Menue: Changedetection_IO; Registry: changedetection_io | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/changedetection_io.md](tools/changedetection_io.md) |
| [directus/directus](https://github.com/directus/directus) | Menue: Directus; Registry: directus | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [django/django](https://github.com/django/django) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md), [docs/tutorials/grok-development-tooling.md](tutorials/grok-development-tooling.md) |
| [docker-library/docs](https://github.com/docker-library/docs) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/qwen-development-tooling.md](tutorials/qwen-development-tooling.md) |
| [docker/awesome-compose](https://github.com/docker/awesome-compose) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/qwen-development-tooling.md](tutorials/qwen-development-tooling.md) |
| [docker/build-push-action](https://github.com/docker/build-push-action) | 62er-Katalog: build_push_action | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/manus-language-infrastructure-sources.md](tutorials/manus-language-infrastructure-sources.md) |
| [docker/buildx](https://github.com/docker/buildx) | 62er-Katalog: buildx | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [docker/cli](https://github.com/docker/cli) | 62er-Katalog: docker_cli | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [docker/compose](https://github.com/docker/compose) | 62er-Katalog: compose | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [docker/login-action](https://github.com/docker/login-action) | 62er-Katalog: login_action | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/manus-language-infrastructure-sources.md](tutorials/manus-language-infrastructure-sources.md) |
| [docker/mcp-registry](https://github.com/docker/mcp-registry) | Registry: docker_mcp_registry | [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/docker_mcp_registry.md](tools/registry/docker_mcp_registry.md) |
| [docker/setup-buildx-action](https://github.com/docker/setup-buildx-action) | 62er-Katalog: setup_buildx_action | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/manus-language-infrastructure-sources.md](tutorials/manus-language-infrastructure-sources.md) |
| [docling-project/docling](https://github.com/docling-project/docling) | Menue: Docling; Registry: docling | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [dominikh/go-tools](https://github.com/dominikh/go-tools) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [dortanes/gemini-desktop](https://github.com/dortanes/gemini-desktop) | Menue: Gemini_Desktop_Dortanes_Legacy; Menue: Gemini_Desktop_Dortanes_Source; Registry: gemini_desktop_dortanes; Registry: gemini_desktop_dortanes_source | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/gemini-desktop-clients.md](tools/gemini-desktop-clients.md) |
| [dotenv-linter/dotenv-linter](https://github.com/dotenv-linter/dotenv-linter) | Keine direkte Zuordnung; manuell pruefen | [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md) |
| [dottxt-ai/outlines](https://github.com/dottxt-ai/outlines) | Menue: Outlines; Registry: outlines | [docs/CREATIVE_LYRICS.md](CREATIVE_LYRICS.md), [docs/tools/SOURCE_INSTALL_READINESS.md](tools/SOURCE_INSTALL_READINESS.md), [docs/tools/outlines.md](tools/outlines.md) |
| [dscripka/openwakeword](https://github.com/dscripka/openwakeword) | Menue: openWakeWord; Registry: openwakeword | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/openwakeword.md](tools/registry/openwakeword.md), [docs/tools/rhasspy-options.md](tools/rhasspy-options.md) |
| [dtolnay/anyhow](https://github.com/dtolnay/anyhow) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md), [docs/tutorials/qwen-development-tooling.md](tutorials/qwen-development-tooling.md) |
| [dtolnay/rust-toolchain](https://github.com/dtolnay/rust-toolchain) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [dtolnay/thiserror](https://github.com/dtolnay/thiserror) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md), [docs/tutorials/qwen-development-tooling.md](tutorials/qwen-development-tooling.md) |
| [duckdb/duckdb](https://github.com/duckdb/duckdb) | Menue: DuckDB; Registry: duckdb | [docs/DUCKDB_INSTALLATION_NOTES.md](DUCKDB_INSTALLATION_NOTES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/duckdb.md](tools/registry/duckdb.md) |
| [duplicati/duplicati](https://github.com/duplicati/duplicati) | Registry: duplicati | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/duplicati.md](tools/registry/duplicati.md) |
| [dwhr-pi/content-multiplier](https://github.com/dwhr-pi/content-multiplier) | Menue: AI_ContentMultiplier; Registry: ai_content_multiplier | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/quality/EXTERNAL_LINK_POLICY.md](quality/EXTERNAL_LINK_POLICY.md) |
| [dwhr-pi/free-vps](https://github.com/dwhr-pi/free-vps) | Keine direkte Zuordnung; manuell pruefen | [docs/VPS_ORACLE_CLOUDFREE_GUIDE.md](VPS_ORACLE_CLOUDFREE_GUIDE.md), [docs/VPS_PROVIDER_ADAPTER.md](VPS_PROVIDER_ADAPTER.md) |
| [dwhr-pi/freevps_by_github-action](https://github.com/dwhr-pi/freevps_by_github-action) | Keine direkte Zuordnung; manuell pruefen | [docs/VPS_PROVIDER_ADAPTER.md](VPS_PROVIDER_ADAPTER.md), [docs/vps/PROVIDER_REVIEW_2026_11_18.md](vps/PROVIDER_REVIEW_2026_11_18.md), [docs/vps/WEEKLY_REVIEW_PROMPT.md](vps/WEEKLY_REVIEW_PROMPT.md) |
| [dwhr-pi/github-vps](https://github.com/dwhr-pi/github-vps) | Keine direkte Zuordnung; manuell pruefen | [docs/VPS_PROVIDER_ADAPTER.md](VPS_PROVIDER_ADAPTER.md), [docs/vps/PROVIDER_REVIEW_2026_11_18.md](vps/PROVIDER_REVIEW_2026_11_18.md), [docs/vps/WEEKLY_REVIEW_PROMPT.md](vps/WEEKLY_REVIEW_PROMPT.md) |
| [dwhr-pi/mynexcloud-for-android](https://github.com/dwhr-pi/mynexcloud-for-android) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/mynextcloud/README.md](tools/mynextcloud/README.md), [docs/tools/mynextcloud/fork_review.md](tools/mynextcloud/fork_review.md), [docs/tools/mynextcloud/install_android_build.md](tools/mynextcloud/install_android_build.md) |
| [dwhr-pi/mynextcloud-server](https://github.com/dwhr-pi/mynextcloud-server) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/mynextcloud/README.md](tools/mynextcloud/README.md), [docs/tools/mynextcloud/fork_review.md](tools/mynextcloud/fork_review.md), [docs/tools/mynextcloud/install_server_vps.md](tools/mynextcloud/install_server_vps.md) |
| [dwhr-pi/openclaw-ai_infrastructure-_ultimate_setup](https://github.com/dwhr-pi/openclaw-ai_infrastructure-_ultimate_setup) | Registry: karaoke_formats; Registry: markdown_docs_server; Registry: personnel_documents | [docs/CI_QA_BOOTSTRAP.md](CI_QA_BOOTSTRAP.md), [docs/CREDENTIALS_BACKUP.md](CREDENTIALS_BACKUP.md), [docs/FORK_SUPPORT_AND_UPSTREAM_GOVERNANCE.md](FORK_SUPPORT_AND_UPSTREAM_GOVERNANCE.md) |
| [dwhr-pi/vps-_kubernate-_ollama_openclaw_installation](https://github.com/dwhr-pi/vps-_kubernate-_ollama_openclaw_installation) | Keine direkte Zuordnung; manuell pruefen | [docs/Profil/alt/KI_Forschung.doc.md](Profil/alt/KI_Forschung.doc.md), [docs/Profil/alt/Programmierer.doc.md](Profil/alt/Programmierer.doc.md), [docs/Profil/alt/Rechtsberatung_Steuerrecht.doc.md](Profil/alt/Rechtsberatung_Steuerrecht.doc.md) |
| [earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad) | Keine direkte Zuordnung; manuell pruefen | [docs/Profile/CAD_Konstrukteur.md](Profile/CAD_Konstrukteur.md) |
| [eclipse-mosquitto/mosquitto](https://github.com/eclipse-mosquitto/mosquitto) | Menue: Mosquitto; Registry: mosquitto | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/MOSQUITTO_INSTALLATION_NOTES.md](MOSQUITTO_INSTALLATION_NOTES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [electron/electron](https://github.com/electron/electron) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [encode/httpx](https://github.com/encode/httpx) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/grok-development-tooling.md](tutorials/grok-development-tooling.md), [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [encode/starlette](https://github.com/encode/starlette) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/grok-development-tooling.md](tutorials/grok-development-tooling.md) |
| [encode/uvicorn](https://github.com/encode/uvicorn) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/grok-development-tooling.md](tutorials/grok-development-tooling.md), [docs/tutorials/manus-development-sources.md](tutorials/manus-development-sources.md), [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [eslint/eslint](https://github.com/eslint/eslint) | 62er-Katalog: eslint | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [espeak-ng/espeak-ng](https://github.com/espeak-ng/espeak-ng) | Menue: eSpeak_NG; Registry: espeak_ng | [docs/tools/SOURCE_INSTALL_READINESS.md](tools/SOURCE_INSTALL_READINESS.md), [docs/tools/espeak-ng.md](tools/espeak-ng.md) |
| [esphome/esphome](https://github.com/esphome/esphome) | Registry: esphome | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/esphome.md](tools/registry/esphome.md) |
| [espressif/esp-claw](https://github.com/espressif/esp-claw) | Keine direkte Zuordnung; manuell pruefen | [docs/research/ESP32_AI_LINUX_AND_OLLAMA.md](research/ESP32_AI_LINUX_AND_OLLAMA.md) |
| [explodinggradients/ragas](https://github.com/explodinggradients/ragas) | Keine direkte Zuordnung; manuell pruefen | [docs/audit/MISSING_TOOLS.md](audit/MISSING_TOOLS.md) |
| [expressjs/express](https://github.com/expressjs/express) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [external-secrets/external-secrets](https://github.com/external-secrets/external-secrets) | Keine direkte Zuordnung; manuell pruefen | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| [facebook/react](https://github.com/facebook/react) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/manus-development-sources.md](tutorials/manus-development-sources.md) |
| [facebookresearch/audiocraft](https://github.com/facebookresearch/audiocraft) | Menue: MusicGen; Registry: audiogen; Registry: musicgen | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/MUSICGEN_INSTALLATION_NOTES.md](MUSICGEN_INSTALLATION_NOTES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [facebookresearch/audioseal](https://github.com/facebookresearch/audioseal) | Registry: audioseal | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_DEEPFAKE_REVIEW.md](media_studio/AUDIO_DEEPFAKE_REVIEW.md) |
| [facebookresearch/demucs](https://github.com/facebookresearch/demucs) | Registry: demucs | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_DEEPFAKE_REVIEW.md](media_studio/AUDIO_DEEPFAKE_REVIEW.md), [docs/tutorials/chatgpt-development-tooling.md](tutorials/chatgpt-development-tooling.md) |
| [fail2ban/fail2ban](https://github.com/fail2ban/fail2ban) | Registry: fail2ban | [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [fal-ai/fal](https://github.com/fal-ai/fal) | Registry: fal_client | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/SOCIAL_AVATAR_AUTOMATION.md](media_studio/SOCIAL_AVATAR_AUTOMATION.md), [docs/tools/fal-client.md](tools/fal-client.md) |
| [falcosecurity/falco](https://github.com/falcosecurity/falco) | Registry: falco | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md), [docs/audit/MISSING_TOOLS.md](audit/MISSING_TOOLS.md) |
| [fanghua-yu/supir](https://github.com/fanghua-yu/supir) | Registry: supir | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/HYBRID_MODELS_AND_WAN.md](media_studio/HYBRID_MODELS_AND_WAN.md), [docs/tools/supir.md](tools/supir.md) |
| [fastapi/fastapi](https://github.com/fastapi/fastapi) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md), [docs/tutorials/grok-development-tooling.md](tutorials/grok-development-tooling.md) |
| [fastapi/sqlmodel](https://github.com/fastapi/sqlmodel) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [fastify/fastify](https://github.com/fastify/fastify) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [fastlane/fastlane](https://github.com/fastlane/fastlane) | Registry: fastlane | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/fastlane.md](tools/registry/fastlane.md) |
| [fatedier/frp](https://github.com/fatedier/frp) | Registry: frp | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/frp.md](tools/registry/frp.md) |
| [ffmpeg/ffmpeg](https://github.com/ffmpeg/ffmpeg) | Registry: ffmpeg | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md), [docs/TOOL_MATRIX.md](TOOL_MATRIX.md) |
| [filebrowser/filebrowser](https://github.com/filebrowser/filebrowser) | Keine direkte Zuordnung; manuell pruefen | [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md) |
| [filosottile/age](https://github.com/filosottile/age) | Registry: age | [docs/CREDENTIALS_BACKUP.md](CREDENTIALS_BACKUP.md), [docs/ENV_VAULT.md](ENV_VAULT.md), [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| [finrandojin/alexandria-audiobook](https://github.com/finrandojin/alexandria-audiobook) | Registry: alexandria_audiobook | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_VIDEO_TOOL_CATALOG.md](media_studio/AUDIO_VIDEO_TOOL_CATALOG.md), [docs/tools/alexandria-audiobook.md](tools/alexandria-audiobook.md) |
| [firecracker-microvm/firecracker](https://github.com/firecracker-microvm/firecracker) | Registry: firecracker | [docs/tools/sandbox-native-candidates.md](tools/sandbox-native-candidates.md), [docs/tools/sandbox-runtimes.md](tools/sandbox-runtimes.md) |
| [fishaudio/fish-speech](https://github.com/fishaudio/fish-speech) | Registry: fish_speech | [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/fish_speech.md](tools/registry/fish_speech.md) |
| [flowiseai/flowise](https://github.com/flowiseai/flowise) | Menue: Flowise; Registry: flowise | [docs/FLOWISE_INSTALLATION_NOTES.md](FLOWISE_INSTALLATION_NOTES.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [flowiseai/flowisechatbot](https://github.com/flowiseai/flowisechatbot) | Keine direkte Zuordnung; manuell pruefen | [docs/FLOWISE_INSTALLATION_NOTES.md](FLOWISE_INSTALLATION_NOTES.md), [docs/quality/EXTERNAL_LINK_POLICY.md](quality/EXTERNAL_LINK_POLICY.md) |
| [flowtyone/comfyui-flowty-triposr](https://github.com/flowtyone/comfyui-flowty-triposr) | Keine direkte Zuordnung; manuell pruefen | [docs/AI_3D_STUDIO.md](AI_3D_STUDIO.md) |
| [fluidsynth/fluidsynth](https://github.com/fluidsynth/fluidsynth) | Keine direkte Zuordnung; manuell pruefen | [docs/models/WAN22_AUDIO_MIDI_TOOLCHAIN.md](models/WAN22_AUDIO_MIDI_TOOLCHAIN.md) |
| [fluxcd/flux2](https://github.com/fluxcd/flux2) | 62er-Katalog: flux_cli; Menue: Flux_CLI; Registry: flux_cli | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [flyway/flyway](https://github.com/flyway/flyway) | 62er-Katalog: flyway | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/manus-language-infrastructure-sources.md](tutorials/manus-language-infrastructure-sources.md) |
| [foundationagents/openmanus](https://github.com/foundationagents/openmanus) | Keine direkte Zuordnung; manuell pruefen | [docs/PROJECT_BRIEF_AND_PROMPT_WORKFLOWS.md](PROJECT_BRIEF_AND_PROMPT_WORKFLOWS.md) |
| [franzdiebold/gen-ai-template](https://github.com/franzdiebold/gen-ai-template) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [freeaihub/ai-lab](https://github.com/freeaihub/ai-lab) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [freecad/freecad](https://github.com/freecad/freecad) | Keine direkte Zuordnung; manuell pruefen | [docs/Profile/CAD_Konstrukteur.md](Profile/CAD_Konstrukteur.md) |
| [freellms/awesome-freellm-apis](https://github.com/freellms/awesome-freellm-apis) | Keine direkte Zuordnung; manuell pruefen | [docs/_API-Keys/FREE_TIERS_AND_TRIAL_CREDITS.md](_API-Keys/FREE_TIERS_AND_TRIAL_CREDITS.md), [docs/_API-Keys/reviews/2026-10-21.md](_API-Keys/reviews/2026-10-21.md), [docs/_API-Keys/reviews/2026-10-26.md](_API-Keys/reviews/2026-10-26.md) |
| [fudan-generative-vision/hallo2](https://github.com/fudan-generative-vision/hallo2) | Registry: hallo2 | [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/VIDEO_AVATAR_SYSTEMS.md](VIDEO_AVATAR_SYSTEMS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [funaudiollm/cosyvoice](https://github.com/funaudiollm/cosyvoice) | Keine direkte Zuordnung; manuell pruefen | [docs/models/WAN22_AUDIO_MIDI_TOOLCHAIN.md](models/WAN22_AUDIO_MIDI_TOOLCHAIN.md) |
| [gcc-mirror/gcc](https://github.com/gcc-mirror/gcc) | 62er-Katalog: gcc_github_mirror | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [geopandas/geopandas](https://github.com/geopandas/geopandas) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [getsops/sops](https://github.com/getsops/sops) | Registry: sops | [docs/SECURE_CORE_REFACTOR.md](SECURE_CORE_REFACTOR.md), [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md) |
| [ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp) | Registry: llama_cpp | [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/llama_cpp.md](tools/registry/llama_cpp.md) |
| [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp) | Keine direkte Zuordnung; manuell pruefen | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md) |
| [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | Menue: Llama_CPP_Toolchain | [docs/MODEL_ROUTING_EXPORT_AND_MONITORING.md](MODEL_ROUTING_EXPORT_AND_MONITORING.md), [docs/Profil/LLM-Builder.doc.md](Profil/LLM-Builder.doc.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md) |
| [ggml-org/whisper.cpp](https://github.com/ggml-org/whisper.cpp) | Menue: Whisper_CPP | [docs/WHISPER_CPP_INSTALLATION_NOTES.md](WHISPER_CPP_INSTALLATION_NOTES.md), [docs/reviews/2026-10-26-platform-patch-plan.md](reviews/2026-10-26-platform-patch-plan.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [gin-gonic/gin](https://github.com/gin-gonic/gin) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [git/git](https://github.com/git/git) | Registry: git | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/git.md](tools/registry/git.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [gitleaks/gitleaks](https://github.com/gitleaks/gitleaks) | Menue: Gitleaks; Registry: gitleaks | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| [giuliano-t/openai-to-freecad-workflow](https://github.com/giuliano-t/openai-to-freecad-workflow) | Keine direkte Zuordnung; manuell pruefen | [docs/Profile/CAD_Konstrukteur.md](Profile/CAD_Konstrukteur.md) |
| [go-chi/chi](https://github.com/go-chi/chi) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [go-delve/delve](https://github.com/go-delve/delve) | 62er-Katalog: delve; Registry: delve | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md) |
| [go-gorm/gorm](https://github.com/go-gorm/gorm) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [go-vikunja/vikunja](https://github.com/go-vikunja/vikunja) | Menue: Vikunja; Registry: vikunja | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [goauthentik/authentik](https://github.com/goauthentik/authentik) | Keine direkte Zuordnung; manuell pruefen | [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md) |
| [godotengine/godot](https://github.com/godotengine/godot) | Menue: Godot_Build; Menue: Godot_Source; Registry: godot_build; Registry: godot_source | [docs/Profile/GameDev_3D_Studio.md](Profile/GameDev_3D_Studio.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [godotengine/godot-demo-projects](https://github.com/godotengine/godot-demo-projects) | Keine direkte Zuordnung; manuell pruefen | [docs/Profile/GameDev_3D_Studio.md](Profile/GameDev_3D_Studio.md) |
| [godotengine/godot-docs](https://github.com/godotengine/godot-docs) | Keine direkte Zuordnung; manuell pruefen | [docs/quality/PR24_LINKCHECK_2026-11-11.md](quality/PR24_LINKCHECK_2026-11-11.md), [docs/tools/ai-game-engines-xr-wallpaper.md](tools/ai-game-engines-xr-wallpaper.md) |
| [godotvr/godot-xr-tools](https://github.com/godotvr/godot-xr-tools) | Menue: Godot_XR_Tools; Registry: godot_xr_tools | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/ai-game-engines-xr-wallpaper.md](tools/ai-game-engines-xr-wallpaper.md) |
| [gofiber/fiber](https://github.com/gofiber/fiber) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [golang-migrate/migrate](https://github.com/golang-migrate/migrate) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/qwen-development-tooling.md](tutorials/qwen-development-tooling.md) |
| [golang-standards/project-layout](https://github.com/golang-standards/project-layout) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/qwen-development-tooling.md](tutorials/qwen-development-tooling.md) |
| [golang-standards/project-template](https://github.com/golang-standards/project-template) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/qwen-development-tooling.md](tutorials/qwen-development-tooling.md) |
| [golang/go](https://github.com/golang/go) | 62er-Katalog: go | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [golang/tools](https://github.com/golang/tools) | 62er-Katalog: golang_tools; Registry: gopls | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md) |
| [golangci/golangci-lint](https://github.com/golangci/golangci-lint) | 62er-Katalog: golangci_lint; Registry: golangci_lint | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md) |
| [golangci/golangci-lint-action](https://github.com/golangci/golangci-lint-action) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | Registry: gemini_cli | [docs/agents/CODING_AGENT_INVENTORY.md](agents/CODING_AGENT_INVENTORY.md), [docs/agents/coding-agent-profiles.md](agents/coding-agent-profiles.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [google-research/frame-interpolation](https://github.com/google-research/frame-interpolation) | Registry: film | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/HYBRID_MODELS_AND_WAN.md](media_studio/HYBRID_MODELS_AND_WAN.md), [docs/tools/film.md](tools/film.md) |
| [google/cadvisor](https://github.com/google/cadvisor) | Menue: cAdvisor; Registry: cadvisor | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [google/googletest](https://github.com/google/googletest) | 62er-Katalog: googletest | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [google/gvisor](https://github.com/google/gvisor) | Registry: gvisor | [docs/INFRASTRUCTURE_REVIEW_2026-11-07.md](INFRASTRUCTURE_REVIEW_2026-11-07.md), [docs/tools/sandbox-native-candidates.md](tools/sandbox-native-candidates.md), [docs/tools/sandbox-runtimes.md](tools/sandbox-runtimes.md) |
| [googleapis/python-genai](https://github.com/googleapis/python-genai) | Registry: veo_api | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/SOCIAL_AVATAR_AUTOMATION.md](media_studio/SOCIAL_AVATAR_AUTOMATION.md), [docs/tools/veo-api.md](tools/veo-api.md) |
| [googlecontainertools/skaffold](https://github.com/googlecontainertools/skaffold) | 62er-Katalog: skaffold | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/manus-language-infrastructure-sources.md](tutorials/manus-language-infrastructure-sources.md) |
| [gradio-app/gradio](https://github.com/gradio-app/gradio) | Menue: Gradio; Registry: gradio | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/EDITABLE_VIDEO_WORKFLOWS.md](media_studio/EDITABLE_VIDEO_WORKFLOWS.md), [docs/tools/github-gap-tools.md](tools/github-gap-tools.md) |
| [gradle/gradle](https://github.com/gradle/gradle) | Registry: gradle | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/gradle.md](tools/registry/gradle.md) |
| [gradle/gradle-distributions](https://github.com/gradle/gradle-distributions) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/security-data-native.md](tools/security-data-native.md) |
| [grafana-community/helm-charts](https://github.com/grafana-community/helm-charts) | Keine direkte Zuordnung; manuell pruefen | [docs/LLMOPS_GPU_AND_OPERATIONS.md](LLMOPS_GPU_AND_OPERATIONS.md) |
| [grafana/alloy](https://github.com/grafana/alloy) | Menue: Grafana_Alloy; Registry: grafana_alloy | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [grafana/grafana](https://github.com/grafana/grafana) | Menue: Grafana; Registry: grafana | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md) |
| [grafana/loki](https://github.com/grafana/loki) | Menue: Loki; Menue: Promtail; Registry: loki; Registry: promtail | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md) |
| [grafana/tempo](https://github.com/grafana/tempo) | Keine direkte Zuordnung; manuell pruefen | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md), [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md), [docs/reviews/2026-10-26-platform-patch-plan.md](reviews/2026-10-26-platform-patch-plan.md) |
| [grpc/grpc-go](https://github.com/grpc/grpc-go) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [gruntwork-io/terratest](https://github.com/gruntwork-io/terratest) | 62er-Katalog: terratest | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/manus-language-infrastructure-sources.md](tutorials/manus-language-infrastructure-sources.md) |
| [guardrails-ai/guardrails](https://github.com/guardrails-ai/guardrails) | Menue: Guardrails_AI; Registry: guardrails_ai | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/guardrails_ai.md](tools/registry/guardrails_ai.md) |
| [guoyww/animatediff](https://github.com/guoyww/animatediff) | Keine direkte Zuordnung; manuell pruefen | [docs/media_studio/SOCIAL_AVATAR_AUTOMATION.md](media_studio/SOCIAL_AVATAR_AUTOMATION.md) |
| [hadolint/hadolint](https://github.com/hadolint/hadolint) | 62er-Katalog: hadolint; Menue: Hadolint | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md) |
| [haoheliu/audioldm2](https://github.com/haoheliu/audioldm2) | Registry: audioldm2 | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_VIDEO_TOOL_CATALOG.md](media_studio/AUDIO_VIDEO_TOOL_CATALOG.md), [docs/tools/audioldm2.md](tools/audioldm2.md) |
| [hashicorp/setup-terraform](https://github.com/hashicorp/setup-terraform) | 62er-Katalog: setup_terraform_action | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/manus-language-infrastructure-sources.md](tutorials/manus-language-infrastructure-sources.md) |
| [hashicorp/terraform](https://github.com/hashicorp/terraform) | 62er-Katalog: terraform | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [hashicorp/terraform-ls](https://github.com/hashicorp/terraform-ls) | 62er-Katalog: terraform_language_server | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/manus-language-infrastructure-sources.md](tutorials/manus-language-infrastructure-sources.md) |
| [hashicorp/vault](https://github.com/hashicorp/vault) | Menue: Vault; Registry: vault | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [healthchecks/healthchecks](https://github.com/healthchecks/healthchecks) | Menue: Healthchecks; Registry: healthchecks | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [hellisotherpeople/constrained-text-generation-studio](https://github.com/hellisotherpeople/constrained-text-generation-studio) | Menue: CTGS; Registry: ctgs | [docs/MUSIC_LYRICS_MODEL_CATALOG.md](MUSIC_LYRICS_MODEL_CATALOG.md), [docs/tools/ctgs.md](tools/ctgs.md) |
| [helm/helm](https://github.com/helm/helm) | 62er-Katalog: helm; Menue: Helm; Registry: helm | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/HELM_INSTALLATION_NOTES.md](HELM_INSTALLATION_NOTES.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md) |
| [henrygd/beszel](https://github.com/henrygd/beszel) | Registry: beszel | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/beszel.md](tools/registry/beszel.md) |
| [hexgrad/kokoro](https://github.com/hexgrad/kokoro) | Registry: kokoro_tts | [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/kokoro_tts.md](tools/registry/kokoro_tts.md) |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | Menue: HyperFrames; Registry: hyperframes | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/hyperframes.md](tools/hyperframes.md), [docs/tools/openmontage.md](tools/openmontage.md) |
| [higgsfield-ai/cli](https://github.com/higgsfield-ai/cli) | Keine direkte Zuordnung; manuell pruefen | [docs/Profile/OpenHiggsStack_AI_Cinema_Studio.md](Profile/OpenHiggsStack_AI_Cinema_Studio.md) |
| [higgsfield-ai/skills](https://github.com/higgsfield-ai/skills) | Keine direkte Zuordnung; manuell pruefen | [docs/Profile/OpenHiggsStack_AI_Cinema_Studio.md](Profile/OpenHiggsStack_AI_Cinema_Studio.md) |
| [hiyouga/llama-factory](https://github.com/hiyouga/llama-factory) | Menue: LLaMA_Factory | [docs/Profil/LLM-Builder.doc.md](Profil/LLM-Builder.doc.md) |
| [home-assistant/core](https://github.com/home-assistant/core) | Menue: Home_Assistant; Registry: home_assistant | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [hpcaitech/open-sora](https://github.com/hpcaitech/open-sora) | Keine direkte Zuordnung; manuell pruefen | [docs/media_studio/VIDEO_TRAINING_DATASETS.md](media_studio/VIDEO_TRAINING_DATASETS.md) |
| [huggingface/accelerate](https://github.com/huggingface/accelerate) | Registry: hf_accelerate | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [huggingface/datasets](https://github.com/huggingface/datasets) | Registry: hf_datasets | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/VIDEO_TRAINING_DATASETS.md](media_studio/VIDEO_TRAINING_DATASETS.md) |
| [huggingface/diffusers](https://github.com/huggingface/diffusers) | Keine direkte Zuordnung; manuell pruefen | [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md) |
| [huggingface/huggingface_hub](https://github.com/huggingface/huggingface_hub) | Registry: hf_hub | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/VIDEO_TRAINING_DATASETS.md](media_studio/VIDEO_TRAINING_DATASETS.md) |
| [huggingface/text-generation-inference](https://github.com/huggingface/text-generation-inference) | Registry: tgi | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/SOCIAL_AVATAR_AUTOMATION.md](media_studio/SOCIAL_AVATAR_AUTOMATION.md) |
| [huggingface/transformers](https://github.com/huggingface/transformers) | Keine direkte Zuordnung; manuell pruefen | [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md) |
| [huginn/huginn](https://github.com/huginn/huginn) | Menue: Huginn; Registry: huginn | [docs/HUGINN_REPO_REF_GUIDE.md](HUGINN_REPO_REF_GUIDE.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/_API-Keys/API_KEY_GUIDE.md](_API-Keys/API_KEY_GUIDE.md) |
| [humanaigc/emo](https://github.com/humanaigc/emo) | Registry: emo_avatar | [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/VIDEO_AVATAR_SYSTEMS.md](VIDEO_AVATAR_SYSTEMS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [hypothesisworks/hypothesis](https://github.com/hypothesisworks/hypothesis) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/grok-development-tooling.md](tutorials/grok-development-tooling.md), [docs/tutorials/manus-development-sources.md](tutorials/manus-development-sources.md) |
| [hzwer/eccv2022-rife](https://github.com/hzwer/eccv2022-rife) | Menue: RIFE; Registry: rife | [docs/RIFE_INSTALLATION_NOTES.md](RIFE_INSTALLATION_NOTES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [ibotpeaches/apktool](https://github.com/ibotpeaches/apktool) | Registry: apktool | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/apktool.md](tools/registry/apktool.md) |
| [iejmac/video2dataset](https://github.com/iejmac/video2dataset) | Menue: Video2Dataset; Registry: video2dataset | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/VIDEO_TRAINING_DATASETS.md](media_studio/VIDEO_TRAINING_DATASETS.md) |
| [igorshubovych/markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli) | Registry: markdownlint_cli | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/markdownlint_cli.md](tools/registry/markdownlint_cli.md) |
| [infiniflow/ragflow](https://github.com/infiniflow/ragflow) | Keine direkte Zuordnung; manuell pruefen | [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md) |
| [infisical/infisical](https://github.com/infisical/infisical) | Registry: infisical | [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/infisical.md](tools/registry/infisical.md) |
| [invoke-ai/invokeai](https://github.com/invoke-ai/invokeai) | Menue: InvokeAI; Registry: invokeai | [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/invokeai.md](tools/registry/invokeai.md) |
| [jackc/pgservicefile](https://github.com/jackc/pgservicefile) | Keine direkte Zuordnung; manuell pruefen | [docs/CLAWBAKE_INTEGRATION_GUIDE.md](CLAWBAKE_INTEGRATION_GUIDE.md), [docs/SETUP_MEMORY.md](SETUP_MEMORY.md) |
| [jackc/pgx](https://github.com/jackc/pgx) | Keine direkte Zuordnung; manuell pruefen | [docs/CLAWBAKE_INTEGRATION_GUIDE.md](CLAWBAKE_INTEGRATION_GUIDE.md) |
| [jaegertracing/jaeger](https://github.com/jaegertracing/jaeger) | Keine direkte Zuordnung; manuell pruefen | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md), [docs/reviews/2026-10-26-platform-patch-plan.md](reviews/2026-10-26-platform-patch-plan.md) |
| [jakeschincariol/youtube-agent-skill](https://github.com/jakeschincariol/youtube-agent-skill) | Registry: youtube_agent_skill | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [janhq/jan](https://github.com/janhq/jan) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [jestjs/jest](https://github.com/jestjs/jest) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/claude-development-tooling.md](tutorials/claude-development-tooling.md), [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [jgm/pandoc](https://github.com/jgm/pandoc) | Registry: pandoc | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/pandoc.md](tools/registry/pandoc.md) |
| [jitsi/jitsi-meet](https://github.com/jitsi/jitsi-meet) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/webinar-stack.md](tutorials/webinar-stack.md) |
| [jpoliv/wakeonlan](https://github.com/jpoliv/wakeonlan) | Registry: wakeonlan | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/wakeonlan.md](tools/registry/wakeonlan.md) |
| [jqlang/jq](https://github.com/jqlang/jq) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [juanfont/headscale](https://github.com/juanfont/headscale) | Registry: headscale | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md) |
| [jub0t/concat](https://github.com/jub0t/concat) | Menue: Concat; Registry: concat | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/concat.md](tools/concat.md) |
| [jupyter/notebook](https://github.com/jupyter/notebook) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/manus-development-sources.md](tutorials/manus-development-sources.md) |
| [jupyterlab/jupyterlab](https://github.com/jupyterlab/jupyterlab) | Menue: JupyterLab; Registry: jupyterlab | [docs/JUPYTERLAB_INSTALLATION_NOTES.md](JUPYTERLAB_INSTALLATION_NOTES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/jupyterlab.md](tools/registry/jupyterlab.md) |
| [justdubit/just-dub-it](https://github.com/justdubit/just-dub-it) | Registry: just_dub_it | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_VIDEO_TOOL_CATALOG.md](media_studio/AUDIO_VIDEO_TOOL_CATALOG.md) |
| [justvugg/colibri](https://github.com/justvugg/colibri) | Registry: colibri | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [k3d-io/k3d](https://github.com/k3d-io/k3d) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [k3s-io/k3s](https://github.com/k3s-io/k3s) | Menue: GitOps_Bootstrap; Registry: gitops_bootstrap; Registry: k3s | [docs/P0_B_CORE_SOURCES.md](P0_B_CORE_SOURCES.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md) |
| [karpathy/llama2.c](https://github.com/karpathy/llama2.c) | Keine direkte Zuordnung; manuell pruefen | [docs/research/ESP32_AI_LINUX_AND_OLLAMA.md](research/ESP32_AI_LINUX_AND_OLLAMA.md) |
| [kata-containers/kata-containers](https://github.com/kata-containers/kata-containers) | Registry: kata_containers | [docs/tools/sandbox-native-candidates.md](tools/sandbox-native-candidates.md), [docs/tools/sandbox-runtimes.md](tools/sandbox-runtimes.md) |
| [kedacore/keda](https://github.com/kedacore/keda) | Registry: keda | [docs/reviews/2026-10-26-platform-patch-plan.md](reviews/2026-10-26-platform-patch-plan.md), [docs/tools/native-go-controllers.md](tools/native-go-controllers.md) |
| [kijai/comfyui-wanvideowrapper](https://github.com/kijai/comfyui-wanvideowrapper) | Menue: WanVideoWrapper; Registry: wanvideo_wrapper | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/HYBRID_MODELS_AND_WAN.md](media_studio/HYBRID_MODELS_AND_WAN.md), [docs/tools/github-gap-tools.md](tools/github-gap-tools.md) |
| [kitware/cmake](https://github.com/kitware/cmake) | 62er-Katalog: cmake | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [klingairesearch/liveportrait](https://github.com/klingairesearch/liveportrait) | Keine direkte Zuordnung; manuell pruefen | [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/VIDEO_AVATAR_SYSTEMS.md](VIDEO_AVATAR_SYSTEMS.md) |
| [kludex/starlette](https://github.com/kludex/starlette) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/grok-development-tooling.md](tutorials/grok-development-tooling.md), [docs/tutorials/manus-development-sources.md](tutorials/manus-development-sources.md) |
| [kludex/uvicorn](https://github.com/kludex/uvicorn) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/manus-development-sources.md](tutorials/manus-development-sources.md) |
| [knadh/listmonk](https://github.com/knadh/listmonk) | Registry: listmonk | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/webinar-tools.md](tools/webinar-tools.md), [docs/tutorials/webinar-stack.md](tutorials/webinar-stack.md) |
| [koalaman/shellcheck](https://github.com/koalaman/shellcheck) | 62er-Katalog: shellcheck | [docs/AUDIT_2026-10-23.md](AUDIT_2026-10-23.md), [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md) |
| [koenkk/zigbee2mqtt](https://github.com/koenkk/zigbee2mqtt) | Menue: Zigbee2MQTT; Registry: zigbee2mqtt | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/zigbee2mqtt.md](tools/zigbee2mqtt.md) |
| [kopia/kopia](https://github.com/kopia/kopia) | Registry: kopia | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/kopia.md](tools/registry/kopia.md) |
| [kozea/radicale](https://github.com/kozea/radicale) | Registry: radicale | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/radicale.md](tools/registry/radicale.md) |
| [kubernetes-sigs/external-dns](https://github.com/kubernetes-sigs/external-dns) | Registry: external_dns | [docs/tools/native-go-controllers.md](tools/native-go-controllers.md) |
| [kubernetes-sigs/gateway-api](https://github.com/kubernetes-sigs/gateway-api) | Keine direkte Zuordnung; manuell pruefen | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| [kubernetes-sigs/kind](https://github.com/kubernetes-sigs/kind) | 62er-Katalog: kind | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [kubernetes-sigs/kustomize](https://github.com/kubernetes-sigs/kustomize) | 62er-Katalog: kustomize; Menue: Kustomize; Registry: kustomize | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/KUSTOMIZE_INSTALLATION_NOTES.md](KUSTOMIZE_INSTALLATION_NOTES.md), [docs/PRODUCTION_BASELINE_CODE.md](PRODUCTION_BASELINE_CODE.md) |
| [kubernetes/examples](https://github.com/kubernetes/examples) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/qwen-development-tooling.md](tutorials/qwen-development-tooling.md) |
| [kubernetes/ingress-nginx](https://github.com/kubernetes/ingress-nginx) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/qwen-development-tooling.md](tutorials/qwen-development-tooling.md) |
| [kubernetes/kube-state-metrics](https://github.com/kubernetes/kube-state-metrics) | Keine direkte Zuordnung; manuell pruefen | [docs/ARCHITECTURE_REVIEW_2026-10-25.md](ARCHITECTURE_REVIEW_2026-10-25.md) |
| [kubernetes/kubectl](https://github.com/kubernetes/kubectl) | 62er-Katalog: kubectl | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) | Menue: Kubectl; Registry: kubectl | [docs/KUBECTL_INSTALLATION_NOTES.md](KUBECTL_INSTALLATION_NOTES.md), [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [kubescape/kubescape](https://github.com/kubescape/kubescape) | Registry: kubescape | [docs/tools/native-security-candidates.md](tools/native-security-candidates.md) |
| [kwaivgi/liveportrait](https://github.com/kwaivgi/liveportrait) | Menue: LivePortrait; Registry: liveportrait | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/github-gap-tools.md](tools/github-gap-tools.md) |
| [kyutai-labs/moshi](https://github.com/kyutai-labs/moshi) | Registry: moshi | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_VIDEO_TOOL_CATALOG.md](media_studio/AUDIO_VIDEO_TOOL_CATALOG.md) |
| [kyverno/kyverno](https://github.com/kyverno/kyverno) | Registry: kyverno | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md), [docs/audit/MISSING_TOOLS.md](audit/MISSING_TOOLS.md), [docs/reviews/2026-10-26-platform-patch-plan.md](reviews/2026-10-26-platform-patch-plan.md) |
| [kyverno/policies](https://github.com/kyverno/policies) | Keine direkte Zuordnung; manuell pruefen | [docs/PLATFORM_GAP_IMPLEMENTATION_2026-10-27.md](PLATFORM_GAP_IMPLEMENTATION_2026-10-27.md) |
| [labstack/echo](https://github.com/labstack/echo) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | Registry: langchain | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/langchain.md](tools/registry/langchain.md), [docs/tutorials/manus-interview-2026-10-22.md](tutorials/manus-interview-2026-10-22.md) |
| [langchain-ai/langchainjs](https://github.com/langchain-ai/langchainjs) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | Registry: langgraph | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/audit/MISSING_TOOLS.md](audit/MISSING_TOOLS.md) |
| [langfuse/langfuse](https://github.com/langfuse/langfuse) | Menue: Langfuse; Registry: langfuse | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [langgenius/dify](https://github.com/langgenius/dify) | Keine direkte Zuordnung; manuell pruefen | [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/tutorials/manus-interview-2026-10-22.md](tutorials/manus-interview-2026-10-22.md) |
| [levo-demo/levo](https://github.com/levo-demo/levo) | Menue: LeVo_2; Registry: levo_2 | [docs/MUSIC_LYRICS_MODEL_CATALOG.md](MUSIC_LYRICS_MODEL_CATALOG.md), [docs/tools/levo-2.md](tools/levo-2.md) |
| [lightricks/ltx-2](https://github.com/lightricks/ltx-2) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/just-dub-it.md](tools/just-dub-it.md) |
| [lightricks/ltx-video](https://github.com/lightricks/ltx-video) | Menue: LTX_Video; Registry: ltx_video | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/SOCIAL_AVATAR_AUTOMATION.md](media_studio/SOCIAL_AVATAR_AUTOMATION.md), [docs/media_studio/VIDEO_TRAINING_DATASETS.md](media_studio/VIDEO_TRAINING_DATASETS.md) |
| [lincolnloop/python-qrcode](https://github.com/lincolnloop/python-qrcode) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [linux-audit/audit-userspace](https://github.com/linux-audit/audit-userspace) | Keine direkte Zuordnung; manuell pruefen | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| [liquibase/liquibase](https://github.com/liquibase/liquibase) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [livekit/livekit](https://github.com/livekit/livekit) | Registry: livekit | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/livekit.md](tools/registry/livekit.md) |
| [lively-community/lively](https://github.com/lively-community/lively) | Menue: Lively_Wallpaper_Source; Registry: lively_wallpaper_source | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/ai-game-engines-xr-wallpaper.md](tools/ai-game-engines-xr-wallpaper.md) |
| [lllyasviel/controlnet](https://github.com/lllyasviel/controlnet) | Keine direkte Zuordnung; manuell pruefen | [docs/Profil/Interior_RoomGPT_Designer.md](Profil/Interior_RoomGPT_Designer.md) |
| [lllyasviel/stable-diffusion-webui-forge](https://github.com/lllyasviel/stable-diffusion-webui-forge) | Menue: Stable_Diffusion_WebUI_Forge; Registry: stable_diffusion_webui_forge | [docs/FORGE_INSTALLATION_NOTES.md](FORGE_INSTALLATION_NOTES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [llvm/llvm-project](https://github.com/llvm/llvm-project) | 62er-Katalog: llvm | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [lmms/lmms](https://github.com/lmms/lmms) | Keine direkte Zuordnung; manuell pruefen | [docs/models/WAN22_AUDIO_MIDI_TOOLCHAIN.md](models/WAN22_AUDIO_MIDI_TOOLCHAIN.md) |
| [lobehub/lobe-chat](https://github.com/lobehub/lobe-chat) | Keine direkte Zuordnung; manuell pruefen | [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md) |
| [longhorn/longhorn](https://github.com/longhorn/longhorn) | Keine direkte Zuordnung; manuell pruefen | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| [louislam/uptime-kuma](https://github.com/louislam/uptime-kuma) | Menue: Uptime_Kuma; Registry: uptime_kuma | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md) |
| [lubluniky/esp32-harness](https://github.com/lubluniky/esp32-harness) | Keine direkte Zuordnung; manuell pruefen | [docs/research/ESP32_AI_LINUX_AND_OLLAMA.md](research/ESP32_AI_LINUX_AND_OLLAMA.md) |
| [m-bain/whisperx](https://github.com/m-bain/whisperx) | Registry: whisperx | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_VIDEO_TOOL_CATALOG.md](media_studio/AUDIO_VIDEO_TOOL_CATALOG.md) |
| [mariadb/server](https://github.com/mariadb/server) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [marin-m/songrec](https://github.com/marin-m/songrec) | Menue: SongRec; Registry: songrec | [docs/AUDIO_RECOGNITION_AND_DOMAIN_MODELS.md](AUDIO_RECOGNITION_AND_DOMAIN_MODELS.md), [docs/tools/SOURCE_INSTALL_READINESS.md](tools/SOURCE_INSTALL_READINESS.md), [docs/tools/songrec.md](tools/songrec.md) |
| [markdownlint/markdownlint](https://github.com/markdownlint/markdownlint) | Keine direkte Zuordnung; manuell pruefen | [docs/AUDIT_2026-10-23.md](AUDIT_2026-10-23.md) |
| [marp-team/marp-cli](https://github.com/marp-team/marp-cli) | Menue: Marp; Registry: marp | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/webinar-tools.md](tools/webinar-tools.md), [docs/tutorials/webinar-stack.md](tutorials/webinar-stack.md) |
| [masterworktools/openforge-tutorials](https://github.com/masterworktools/openforge-tutorials) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/gitlab-openforge-mlflow.md](tools/gitlab-openforge-mlflow.md) |
| [mastra-ai/mastra](https://github.com/mastra-ai/mastra) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/grok-development-tooling.md](tutorials/grok-development-tooling.md) |
| [matplotlib/matplotlib](https://github.com/matplotlib/matplotlib) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md), [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [mautic/mautic](https://github.com/mautic/mautic) | Registry: mautic | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/webinar-tools.md](tools/webinar-tools.md), [docs/tutorials/webinar-stack.md](tutorials/webinar-stack.md) |
| [medahmedkrichen/vidubb](https://github.com/medahmedkrichen/vidubb) | Registry: vidubb | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_VIDEO_TOOL_CATALOG.md](media_studio/AUDIO_VIDEO_TOOL_CATALOG.md), [docs/tools/vidubb.md](tools/vidubb.md) |
| [meilisearch/meilisearch](https://github.com/meilisearch/meilisearch) | Menue: Meilisearch; Registry: meilisearch | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md) |
| [mendableai/firecrawl](https://github.com/mendableai/firecrawl) | Keine direkte Zuordnung; manuell pruefen | [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md) |
| [mermaid-js/mermaid](https://github.com/mermaid-js/mermaid) | Keine direkte Zuordnung; manuell pruefen | [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md) |
| [mesonbuild/meson](https://github.com/mesonbuild/meson) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [metabase/metabase](https://github.com/metabase/metabase) | Menue: Metabase; Registry: metabase | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [metallb/metallb](https://github.com/metallb/metallb) | Keine direkte Zuordnung; manuell pruefen | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| `https://github.com/microsoft/agent-framework` (unverifiziert, 2026-11-19) | Registry: agent_framework | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/MULTI_AGENT_AUDIT_2026-11-05.md](audit/MULTI_AGENT_AUDIT_2026-11-05.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [microsoft/autogen](https://github.com/microsoft/autogen) | Registry: autogen | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [microsoft/playwright](https://github.com/microsoft/playwright) | 62er-Katalog: playwright | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [microsoft/playwright-github-action](https://github.com/microsoft/playwright-github-action) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/manus-development-sources.md](tutorials/manus-development-sources.md) |
| [microsoft/presidio](https://github.com/microsoft/presidio) | Keine direkte Zuordnung; manuell pruefen | [docs/legal/RAG_COMPLIANCE_ARCHITECTURE.md](legal/RAG_COMPLIANCE_ARCHITECTURE.md) |
| [microsoft/pylance-release](https://github.com/microsoft/pylance-release) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [microsoft/pyright](https://github.com/microsoft/pyright) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [microsoft/typescript](https://github.com/microsoft/typescript) | 62er-Katalog: typescript | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [microsoft/typescript-node-starter](https://github.com/microsoft/typescript-node-starter) | Keine direkte Zuordnung; manuell pruefen | [docs/quality/EXTERNAL_LINK_POLICY.md](quality/EXTERNAL_LINK_POLICY.md), [docs/tutorials/qwen-development-tooling.md](tutorials/qwen-development-tooling.md) |
| [microsoft/vscode](https://github.com/microsoft/vscode) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/manus-interview-2026-10-22.md](tutorials/manus-interview-2026-10-22.md), [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [mido/mido](https://github.com/mido/mido) | Keine direkte Zuordnung; manuell pruefen | [docs/models/WAN22_AUDIO_MIDI_TOOLCHAIN.md](models/WAN22_AUDIO_MIDI_TOOLCHAIN.md) |
| [milvus-io/milvus](https://github.com/milvus-io/milvus) | Registry: milvus | [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md), [docs/tools/security-data-native.md](tools/security-data-native.md) |
| [minimax-ai/minimax-m3](https://github.com/minimax-ai/minimax-m3) | Menue: MiniMax_M3; Registry: minimax_m3 | [docs/tools/minimax-m3.md](tools/minimax-m3.md) |
| [minio/minio](https://github.com/minio/minio) | Menue: MinIO; Registry: minio | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [mirror/make](https://github.com/mirror/make) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [mitmproxy/mitmproxy](https://github.com/mitmproxy/mitmproxy) | Registry: mitmproxy | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/mitmproxy.md](tools/registry/mitmproxy.md) |
| [mkdocs/mkdocs](https://github.com/mkdocs/mkdocs) | Registry: mkdocs | [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/mkdocs.md](tools/registry/mkdocs.md) |
| [ml-explore/mlx-examples](https://github.com/ml-explore/mlx-examples) | Keine direkte Zuordnung; manuell pruefen | [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md) |
| [mlflow/mlflow](https://github.com/mlflow/mlflow) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/gitlab-openforge-mlflow.md](tools/gitlab-openforge-mlflow.md) |
| [mmorise/world](https://github.com/mmorise/world) | Keine direkte Zuordnung; manuell pruefen | [docs/models/WAN22_AUDIO_MIDI_TOOLCHAIN.md](models/WAN22_AUDIO_MIDI_TOOLCHAIN.md) |
| [mnfst/awesome-free-llm-apis](https://github.com/mnfst/awesome-free-llm-apis) | Keine direkte Zuordnung; manuell pruefen | [docs/_API-Keys/FREE_TIERS_AND_TRIAL_CREDITS.md](_API-Keys/FREE_TIERS_AND_TRIAL_CREDITS.md), [docs/_API-Keys/reviews/2026-10-21.md](_API-Keys/reviews/2026-10-21.md), [docs/_API-Keys/reviews/2026-10-26.md](_API-Keys/reviews/2026-10-26.md) |
| [mobsf/mobile-security-framework-mobsf](https://github.com/mobsf/mobile-security-framework-mobsf) | Keine direkte Zuordnung; manuell pruefen | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md) |
| [moby/buildkit](https://github.com/moby/buildkit) | 62er-Katalog: buildkit | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/manus-language-infrastructure-sources.md](tutorials/manus-language-infrastructure-sources.md) |
| [moby/moby](https://github.com/moby/moby) | Registry: docker | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/claude-development-tooling.md](tutorials/claude-development-tooling.md) |
| [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) | Keine direkte Zuordnung; manuell pruefen | [docs/NATIVE_OPERATIONS_HANDBOOK.md](NATIVE_OPERATIONS_HANDBOOK.md) |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | Registry: mcp_browser; Registry: mcp_browser_server; Registry: mcp_fetch; Registry: mcp_fetch_server; Registry: mcp_filesystem; Registry: mcp_filesystem_server; Registry: mcp_git; Registry: mcp_git_server; Registry: mcp_github; Registry: mcp_github_server; Registry: mcp_memory; Registry: mcp_memory_server; Registry: mcp_postgres; Registry: mcp_postgres_server; Registry: mcp_shell; Registry: mcp_shell_server; Registry: mcp_sqlite; Registry: mcp_sqlite_server; Registry: modelcontextprotocol_servers | [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md), [docs/TOOL_MATRIX.md](TOOL_MATRIX.md) |
| [modelcontextprotocol/servers-archived](https://github.com/modelcontextprotocol/servers-archived) | Keine direkte Zuordnung; manuell pruefen | [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/agents/CI_REPAIR_STATUS.md](agents/CI_REPAIR_STATUS.md), [docs/quality/EXTERNAL_LINK_POLICY.md](quality/EXTERNAL_LINK_POLICY.md) |
| [modelscope/clearervoice-studio](https://github.com/modelscope/clearervoice-studio) | Registry: clearer_voice_studio | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/clearer_voice_studio.md](tools/registry/clearer_voice_studio.md) |
| [modelscope/data-juicer](https://github.com/modelscope/data-juicer) | Menue: Data_Juicer | [docs/Profil/LLM-Builder.doc.md](Profil/LLM-Builder.doc.md) |
| [modimihir07/agentic-os](https://github.com/modimihir07/agentic-os) | Registry: agentic_os | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/agentic-os.md](tools/agentic-os.md) |
| [moonshotai/kimi-cli](https://github.com/moonshotai/kimi-cli) | Keine direkte Zuordnung; manuell pruefen | [docs/PROJECT_BRIEF_AND_PROMPT_WORKFLOWS.md](PROJECT_BRIEF_AND_PROMPT_WORKFLOWS.md) |
| [morluto/rea](https://github.com/morluto/rea) | Registry: rea | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [mudler/localai](https://github.com/mudler/localai) | Registry: localai | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md) |
| [multimodal-art-projection/yue](https://github.com/multimodal-art-projection/yue) | Registry: yue | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_VIDEO_TOOL_CATALOG.md](media_studio/AUDIO_VIDEO_TOOL_CATALOG.md) |
| [mvdan/sh](https://github.com/mvdan/sh) | 62er-Katalog: shfmt; Menue: Shfmt | [docs/AUDIT_2026-10-23.md](AUDIT_2026-10-23.md), [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md) |
| [mwaskom/seaborn](https://github.com/mwaskom/seaborn) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [myshell-ai/melotts](https://github.com/myshell-ai/melotts) | Registry: melotts | [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/melotts.md](tools/registry/melotts.md) |
| [myshell-ai/openvoice](https://github.com/myshell-ai/openvoice) | Registry: openvoice | [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/openvoice.md](tools/registry/openvoice.md) |
| [mysql/mysql-server](https://github.com/mysql/mysql-server) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [n8n-io/n8n](https://github.com/n8n-io/n8n) | Menue: n8n; Registry: n8n | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [n8n-io/self-hosted-ai-starter-kit](https://github.com/n8n-io/self-hosted-ai-starter-kit) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [natooz/miditok](https://github.com/natooz/miditok) | Keine direkte Zuordnung; manuell pruefen | [docs/models/SONGSAGE_MIDI_RESEARCH.md](models/SONGSAGE_MIDI_RESEARCH.md), [docs/models/WAN22_AUDIO_MIDI_TOOLCHAIN.md](models/WAN22_AUDIO_MIDI_TOOLCHAIN.md) |
| [nats-io/nats-server](https://github.com/nats-io/nats-server) | Menue: NATS | [docs/REVIEW-2026-11-11.md](REVIEW-2026-11-11.md) |
| [nedbat/coveragepy](https://github.com/nedbat/coveragepy) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/grok-development-tooling.md](tutorials/grok-development-tooling.md), [docs/tutorials/manus-development-sources.md](tutorials/manus-development-sources.md), [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [neo4j/neo4j](https://github.com/neo4j/neo4j) | Menue: Neo4j; Registry: neo4j | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [nestjs/nest](https://github.com/nestjs/nest) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [netblue30/firejail](https://github.com/netblue30/firejail) | Registry: firejail | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/firejail.md](tools/registry/firejail.md) |
| [netdata/netdata](https://github.com/netdata/netdata) | Menue: Netdata; Registry: netdata | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md) |
| [netflix/void-model](https://github.com/netflix/void-model) | Registry: void_model | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_VIDEO_TOOL_CATALOG.md](media_studio/AUDIO_VIDEO_TOOL_CATALOG.md) |
| [neurometricai/clawbake](https://github.com/neurometricai/clawbake) | Menue: Clawbake | [docs/CLAWBAKE_INTEGRATION_GUIDE.md](CLAWBAKE_INTEGRATION_GUIDE.md), [docs/SETUP_MEMORY.md](SETUP_MEMORY.md) |
| [nextcloud/android](https://github.com/nextcloud/android) | Keine direkte Zuordnung; manuell pruefen | [docs/Profile/mynextcloud_android.md](Profile/mynextcloud_android.md), [docs/tools/mynextcloud/README.md](tools/mynextcloud/README.md), [docs/tools/mynextcloud/fork_review.md](tools/mynextcloud/fork_review.md) |
| [nextcloud/android-library](https://github.com/nextcloud/android-library) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/mynextcloud/README.md](tools/mynextcloud/README.md), [docs/tools/mynextcloud/fork_review.md](tools/mynextcloud/fork_review.md), [docs/tools/mynextcloud/legal_branding_checklist.md](tools/mynextcloud/legal_branding_checklist.md) |
| [nextcloud/nextcloudpi](https://github.com/nextcloud/nextcloudpi) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/mynextcloud/README.md](tools/mynextcloud/README.md), [docs/tools/mynextcloud/fork_review.md](tools/mynextcloud/fork_review.md) |
| [nextcloud/server](https://github.com/nextcloud/server) | Menue: Nextcloud; Registry: nextcloud | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/TOOL_INDEX.md](TOOL_INDEX.md) |
| [nextest-rs/nextest](https://github.com/nextest-rs/nextest) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [nginxproxymanager/nginx-proxy-manager](https://github.com/nginxproxymanager/nginx-proxy-manager) | Registry: nginx_proxy_manager | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/nginx_proxy_manager.md](tools/registry/nginx_proxy_manager.md) |
| [nicolargo/glances](https://github.com/nicolargo/glances) | Registry: glances | [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/glances.md](tools/registry/glances.md) |
| [nightroman/invoke-build](https://github.com/nightroman/invoke-build) | 62er-Katalog: invoke_build; Registry: invoke_build | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md) |
| [ninja-build/ninja](https://github.com/ninja-build/ninja) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [nmap/nmap](https://github.com/nmap/nmap) | Registry: nmap | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/nmap.md](tools/registry/nmap.md) |
| [nnsvs/nnsvs](https://github.com/nnsvs/nnsvs) | Registry: nnsvs | [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/nnsvs.md](tools/registry/nnsvs.md) |
| [nocodb/nocodb](https://github.com/nocodb/nocodb) | Menue: NocoDB; Registry: nocodb | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [node-red/node-red](https://github.com/node-red/node-red) | Menue: Node_Red; Registry: node_red | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md) |
| [nodejs/corepack](https://github.com/nodejs/corepack) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/qwen-code.md](tools/qwen-code.md) |
| [nodejs/node](https://github.com/nodejs/node) | 62er-Katalog: node_js | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tools/development-toolchain-check.md](tools/development-toolchain-check.md) |
| [nousresearch/hermes-agent](https://github.com/nousresearch/hermes-agent) | Menue: Hermes_Agent_Jarvis; Registry: hermes_agent_jarvis | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/github-gap-tools.md](tools/github-gap-tools.md), [docs/tools/hermes-jarvis-weekend.md](tools/hermes-jarvis-weekend.md) |
| [numpy/numpy](https://github.com/numpy/numpy) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/manus-development-workflow.md](tutorials/manus-development-workflow.md), [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [nuprl/multipl-e](https://github.com/nuprl/multipl-e) | Keine direkte Zuordnung; manuell pruefen | [docs/models/TRAINING_AND_EVALUATION.md](models/TRAINING_AND_EVALUATION.md) |
| [nutlope/roomgpt](https://github.com/nutlope/roomgpt) | Keine direkte Zuordnung; manuell pruefen | [docs/Profil/Interior_RoomGPT_Designer.md](Profil/Interior_RoomGPT_Designer.md) |
| [nvidia/dcgm](https://github.com/nvidia/dcgm) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-development-tooling.md](tutorials/chatgpt-development-tooling.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [nvidia/dcgm-exporter](https://github.com/nvidia/dcgm-exporter) | Keine direkte Zuordnung; manuell pruefen | [docs/ARCHITECTURE_REVIEW_2026-10-25.md](ARCHITECTURE_REVIEW_2026-10-25.md), [docs/INFRASTRUCTURE_REVIEW_2026-11-07.md](INFRASTRUCTURE_REVIEW_2026-11-07.md), [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| [nvidia/k8s-device-plugin](https://github.com/nvidia/k8s-device-plugin) | Keine direkte Zuordnung; manuell pruefen | [docs/ARCHITECTURE_REVIEW_2026-10-25.md](ARCHITECTURE_REVIEW_2026-10-25.md), [docs/LLMOPS_GPU_AND_OPERATIONS.md](LLMOPS_GPU_AND_OPERATIONS.md), [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| [nvm-sh/nvm](https://github.com/nvm-sh/nvm) | Keine direkte Zuordnung; manuell pruefen | [docs/PUPPETEER_INSTALLATION_NOTES.md](PUPPETEER_INSTALLATION_NOTES.md) |
| [o3de/o3de](https://github.com/o3de/o3de) | Menue: O3DE_Source; Registry: o3de_source | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/ai-game-engines-xr-wallpaper.md](tools/ai-game-engines-xr-wallpaper.md) |
| [o3de/o3de-extras](https://github.com/o3de/o3de-extras) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/ai-game-engines-xr-wallpaper.md](tools/ai-game-engines-xr-wallpaper.md) |
| [obot-platform/obot](https://github.com/obot-platform/obot) | Menue: Obot; Registry: obot | [docs/HYBRID_CLOUD_MCP.md](HYBRID_CLOUD_MCP.md), [docs/tools/SOURCE_INSTALL_READINESS.md](tools/SOURCE_INSTALL_READINESS.md), [docs/tools/obot.md](tools/obot.md) |
| [obsproject/obs-studio](https://github.com/obsproject/obs-studio) | Menue: OBS; Registry: obs | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/github-gap-tools.md](tools/github-gap-tools.md), [docs/tutorials/webinar-stack.md](tutorials/webinar-stack.md) |
| [ocrmypdf/ocrmypdf](https://github.com/ocrmypdf/ocrmypdf) | Registry: ocrmypdf | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/ocrmypdf.md](tools/registry/ocrmypdf.md) |
| [ohf-voice/linux-voice-assistant](https://github.com/ohf-voice/linux-voice-assistant) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/rhasspy-options.md](tools/rhasspy-options.md) |
| [ohf-voice/piper1-gpl](https://github.com/ohf-voice/piper1-gpl) | Keine direkte Zuordnung; manuell pruefen | [docs/reviews/2026-10-26-platform-patch-plan.md](reviews/2026-10-26-platform-patch-plan.md), [docs/tools/rhasspy-options.md](tools/rhasspy-options.md), [docs/tutorials/chatgpt-development-tooling.md](tutorials/chatgpt-development-tooling.md) |
| [oisf/suricata](https://github.com/oisf/suricata) | Registry: suricata | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/suricata.md](tools/registry/suricata.md) |
| [ollama/ollama](https://github.com/ollama/ollama) | Keine direkte Zuordnung; manuell pruefen | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/P0_B_CORE_SOURCES.md](P0_B_CORE_SOURCES.md), [docs/PLATFORM_GAP_IMPLEMENTATION_2026-10-27.md](PLATFORM_GAP_IMPLEMENTATION_2026-10-27.md) |
| [open-jarvis/openjarvis](https://github.com/open-jarvis/openjarvis) | Registry: openjarvis | [docs/tools/openjarvis.md](tools/openjarvis.md) |
| [open-policy-agent/gatekeeper](https://github.com/open-policy-agent/gatekeeper) | Registry: gatekeeper | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md), [docs/reviews/2026-10-26-platform-patch-plan.md](reviews/2026-10-26-platform-patch-plan.md), [docs/tools/native-go-controllers.md](tools/native-go-controllers.md) |
| [open-telemetry/opentelemetry-collector](https://github.com/open-telemetry/opentelemetry-collector) | Menue: OpenTelemetry; Registry: opentelemetry | [docs/DOCKER_REMAINDER_2026-10-27.md](DOCKER_REMAINDER_2026-10-27.md), [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/REVIEW-2026-11-11.md](REVIEW-2026-11-11.md) |
| [open-telemetry/opentelemetry-collector-contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | Keine direkte Zuordnung; manuell pruefen | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| [open-webui/mcpo](https://github.com/open-webui/mcpo) | Menue: MCPO; Registry: mcpo | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/mcpo.md](tools/registry/mcpo.md) |
| [open-webui/open-webui](https://github.com/open-webui/open-webui) | Menue: Open_WebUI; Registry: open_webui | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/NATIVE_OPERATIONS_HANDBOOK.md](NATIVE_OPERATIONS_HANDBOOK.md) |
| [open-webui/openapi-servers](https://github.com/open-webui/openapi-servers) | Menue: OpenAPI_Servers; Registry: openapi_servers | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/openapi-servers.md](tools/openapi-servers.md) |
| [openai/codex](https://github.com/openai/codex) | Menue: Codex_CLI; Registry: codex_cli | [docs/agents/CODING_AGENT_INVENTORY.md](agents/CODING_AGENT_INVENTORY.md), [docs/agents/NATIVE_CLI_BUILDS.md](agents/NATIVE_CLI_BUILDS.md), [docs/audit/MULTI_AGENT_AUDIT_2026-11-05.md](audit/MULTI_AGENT_AUDIT_2026-11-05.md) |
| [openai/gpt-oss](https://github.com/openai/gpt-oss) | Menue: GPT_OSS_120B; Registry: gpt_oss_120b | [docs/AUDIO_RECOGNITION_AND_DOMAIN_MODELS.md](AUDIO_RECOGNITION_AND_DOMAIN_MODELS.md), [docs/tools/gpt-oss-120b.md](tools/gpt-oss-120b.md) |
| [openai/whisper](https://github.com/openai/whisper) | Keine direkte Zuordnung; manuell pruefen | [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md), [docs/tools/rhasspy-options.md](tools/rhasspy-options.md), [docs/tutorials/manus-interview-2026-10-22.md](tutorials/manus-interview-2026-10-22.md) |
| [openbao/openbao](https://github.com/openbao/openbao) | Registry: openbao | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [openclaw/clawbake](https://github.com/openclaw/clawbake) | Keine direkte Zuordnung; manuell pruefen | [docs/CLAWBAKE_INTEGRATION_GUIDE.md](CLAWBAKE_INTEGRATION_GUIDE.md), [docs/SETUP_MEMORY.md](SETUP_MEMORY.md), [docs/quality/EXTERNAL_LINK_POLICY.md](quality/EXTERNAL_LINK_POLICY.md) |
| [openclaw/openclaw](https://github.com/openclaw/openclaw) | Keine direkte Zuordnung; manuell pruefen | [docs/P0_B_CORE_SOURCES.md](P0_B_CORE_SOURCES.md), [docs/_API-Keys/FREE_TIERS_AND_TRIAL_CREDITS.md](_API-Keys/FREE_TIERS_AND_TRIAL_CREDITS.md), [docs/_API-Keys/reviews/2026-10-21.md](_API-Keys/reviews/2026-10-21.md) |
| [opencv/opencv](https://github.com/opencv/opencv) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [opendevin/opendevin](https://github.com/opendevin/opendevin) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/qwen-development-tooling.md](tutorials/qwen-development-tooling.md) |
| [openebs/openebs](https://github.com/openebs/openebs) | Keine direkte Zuordnung; manuell pruefen | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| [openhands/openhands](https://github.com/openhands/openhands) | Keine direkte Zuordnung; manuell pruefen | [docs/agents/CODING_AGENT_INVENTORY.md](agents/CODING_AGENT_INVENTORY.md), [docs/audit/MULTI_AGENT_AUDIT_2026-11-05.md](audit/MULTI_AGENT_AUDIT_2026-11-05.md), [docs/reviews/2026-10-26-platform-patch-plan.md](reviews/2026-10-26-platform-patch-plan.md) |
| [openhands/software-agent-sdk](https://github.com/openhands/software-agent-sdk) | Menue: OpenHands; Registry: openhands | [docs/agents/LOCAL_CODING_WORKBENCH.md](agents/LOCAL_CODING_WORKBENCH.md), [docs/agents/NATIVE_CLI_BUILDS.md](agents/NATIVE_CLI_BUILDS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [openinterpreter/open-interpreter](https://github.com/openinterpreter/open-interpreter) | Keine direkte Zuordnung; manuell pruefen | [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md) |
| [openlit/openlit](https://github.com/openlit/openlit) | Menue: OpenLIT | [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md) |
| [openmanus/openmanus](https://github.com/openmanus/openmanus) | Menue: OpenManus | [docs/legacy/K8S_DEPLOYMENTS_LEGACY.md](legacy/K8S_DEPLOYMENTS_LEGACY.md) |
| [openmoss/moss-music](https://github.com/openmoss/moss-music) | Menue: MOSS_Music; Registry: moss_music | [docs/MUSIC_LYRICS_MODEL_CATALOG.md](MUSIC_LYRICS_MODEL_CATALOG.md), [docs/tools/moss-music.md](tools/moss-music.md) |
| [openmoss/moss-tts](https://github.com/openmoss/moss-tts) | Registry: moss_tts | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_VIDEO_TOOL_CATALOG.md](media_studio/AUDIO_VIDEO_TOOL_CATALOG.md) |
| [openocd-org/openocd](https://github.com/openocd-org/openocd) | Keine direkte Zuordnung; manuell pruefen | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/tools/embedded-debug-hil.md](tools/embedded-debug-hil.md) |
| [openscad/openscad](https://github.com/openscad/openscad) | Keine direkte Zuordnung; manuell pruefen | [docs/Profile/CAD_Konstrukteur.md](Profile/CAD_Konstrukteur.md) |
| [openscap/openscap](https://github.com/openscap/openscap) | Registry: openscap | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/openscap.md](tools/registry/openscap.md) |
| [opentalker/sadtalker](https://github.com/opentalker/sadtalker) | Menue: SadTalker; Registry: sadtalker | [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/VIDEO_AVATAR_SYSTEMS.md](VIDEO_AVATAR_SYSTEMS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [opentofu/opentofu](https://github.com/opentofu/opentofu) | Menue: OpenTofu | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md), [docs/tutorials/manus-language-infrastructure-sources.md](tutorials/manus-language-infrastructure-sources.md) |
| [openutau/openutau](https://github.com/openutau/openutau) | Registry: openutau | [docs/tools/local-audio-chain.md](tools/local-audio-chain.md) |
| [openvpi/diffsinger](https://github.com/openvpi/diffsinger) | Registry: diffsinger | [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/local-audio-chain.md](tools/local-audio-chain.md) |
| [oven-sh/bun](https://github.com/oven-sh/bun) | Menue: Activepieces | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [owner/repository](https://github.com/owner/repository) | Keine direkte Zuordnung; manuell pruefen | [docs/P0_SAFETY_CHANGES.md](P0_SAFETY_CHANGES.md) |
| [paddlepaddle/paddleocr](https://github.com/paddlepaddle/paddleocr) | Registry: paddleocr | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/paddleocr.md](tools/registry/paddleocr.md) |
| [pallets/flask](https://github.com/pallets/flask) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md), [docs/tutorials/grok-development-tooling.md](tutorials/grok-development-tooling.md) |
| [pallets/jinja](https://github.com/pallets/jinja) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/grok-development-tooling.md](tutorials/grok-development-tooling.md) |
| [pandas-dev/pandas](https://github.com/pandas-dev/pandas) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md), [docs/tutorials/manus-development-workflow.md](tutorials/manus-development-workflow.md) |
| [paperless-ngx/paperless-ngx](https://github.com/paperless-ngx/paperless-ngx) | Registry: paperless_ngx | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/SETUP_REVIEW_2026_NEXT_ACTIONS.md](SETUP_REVIEW_2026_NEXT_ACTIONS.md) |
| [penpot/penpot](https://github.com/penpot/penpot) | Menue: Penpot; Registry: penpot | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/Profil/Penpot-MCP-Integration.md](Profil/Penpot-MCP-Integration.md), [docs/Profil/UI-UX-Designer-Penpot-AI.md](Profil/UI-UX-Designer-Penpot-AI.md) |
| [penpot/penpot-mcp](https://github.com/penpot/penpot-mcp) | Keine direkte Zuordnung; manuell pruefen | [docs/Profil/Penpot-MCP-Integration.md](Profil/Penpot-MCP-Integration.md), [docs/Profil/UI-UX-Designer-Penpot-AI.md](Profil/UI-UX-Designer-Penpot-AI.md) |
| [penpot/skia-binaries](https://github.com/penpot/skia-binaries) | Keine direkte Zuordnung; manuell pruefen | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md) |
| [perplexityai/api-cookbook](https://github.com/perplexityai/api-cookbook) | Menue: Perplexity_API_Cookbook; Registry: perplexity_cookbook | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/comet-and-browser-research.md](tools/comet-and-browser-research.md) |
| [perplexityai/modelcontextprotocol](https://github.com/perplexityai/modelcontextprotocol) | Menue: Perplexity_MCP; Registry: perplexity_mcp | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/comet-and-browser-research.md](tools/comet-and-browser-research.md), [docs/tools/perplexity_mcp.md](tools/perplexity_mcp.md) |
| [perplexityai/perplexity-node](https://github.com/perplexityai/perplexity-node) | Menue: Perplexity_Node; Registry: perplexity_node | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/comet-and-browser-research.md](tools/comet-and-browser-research.md), [docs/tools/perplexity-sdk-build.md](tools/perplexity-sdk-build.md) |
| [perplexityai/perplexity-py](https://github.com/perplexityai/perplexity-py) | Menue: Perplexity_Python; Registry: perplexity_python | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/comet-and-browser-research.md](tools/comet-and-browser-research.md), [docs/tools/perplexity-sdk-build.md](tools/perplexity-sdk-build.md) |
| [pester/pester](https://github.com/pester/pester) | 62er-Katalog: pester | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tools/development-toolchain-check.md](tools/development-toolchain-check.md) |
| [pgbackrest/pgbackrest](https://github.com/pgbackrest/pgbackrest) | Keine direkte Zuordnung; manuell pruefen | [docs/reviews/2026-10-26-platform-patch-plan.md](reviews/2026-10-26-platform-patch-plan.md) |
| [pgvector/pgvector](https://github.com/pgvector/pgvector) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/manus-interview-2026-10-22.md](tutorials/manus-interview-2026-10-22.md) |
| [pi-hole/pi-hole](https://github.com/pi-hole/pi-hole) | Keine direkte Zuordnung; manuell pruefen | [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md) |
| [pinokiocomputer/pinokio](https://github.com/pinokiocomputer/pinokio) | Registry: pinokio | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/SOCIAL_AVATAR_AUTOMATION.md](media_studio/SOCIAL_AVATAR_AUTOMATION.md), [docs/tools/pinokio.md](tools/pinokio.md) |
| [plachtaa/seed-vc](https://github.com/plachtaa/seed-vc) | Registry: seed_vc | [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/local-audio-chain.md](tools/local-audio-chain.md) |
| [plotly/plotly.py](https://github.com/plotly/plotly.py) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [pnpm/pnpm](https://github.com/pnpm/pnpm) | 62er-Katalog: pnpm | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tools/perplexity-sdk-build.md](tools/perplexity-sdk-build.md) |
| [pola-rs/polars](https://github.com/pola-rs/polars) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [postgres/postgres](https://github.com/postgres/postgres) | 62er-Katalog: postgres | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md) |
| [powershell/powershell](https://github.com/powershell/powershell) | 62er-Katalog: powershell | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tools/development-toolchain-check.md](tools/development-toolchain-check.md) |
| [powershell/psscriptanalyzer](https://github.com/powershell/psscriptanalyzer) | 62er-Katalog: psscriptanalyzer | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tools/development-toolchain-check.md](tools/development-toolchain-check.md) |
| [powershell/vscode-powershell](https://github.com/powershell/vscode-powershell) | 62er-Katalog: vs_code_powershell | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tools/development-toolchain-check.md](tools/development-toolchain-check.md) |
| [pre-commit/pre-commit](https://github.com/pre-commit/pre-commit) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/manus-development-sources.md](tutorials/manus-development-sources.md), [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [prefecthq/prefect](https://github.com/prefecthq/prefect) | Menue: Prefect; Registry: prefect | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/prefect.md](tools/registry/prefect.md) |
| [prettier/prettier](https://github.com/prettier/prettier) | 62er-Katalog: prettier | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/claude-development-tooling.md](tutorials/claude-development-tooling.md) |
| [prisma/orm](https://github.com/prisma/orm) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-development-tooling.md](tutorials/chatgpt-development-tooling.md), [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [prisma/prisma](https://github.com/prisma/prisma) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-development-tooling.md](tutorials/chatgpt-development-tooling.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [projectdiscovery/nuclei](https://github.com/projectdiscovery/nuclei) | Registry: nuclei | [docs/tools/native-security-candidates.md](tools/native-security-candidates.md) |
| [prometheus-community/helm-charts](https://github.com/prometheus-community/helm-charts) | Keine direkte Zuordnung; manuell pruefen | [docs/LLMOPS_GPU_AND_OPERATIONS.md](LLMOPS_GPU_AND_OPERATIONS.md), [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| [prometheus-community/windows_exporter](https://github.com/prometheus-community/windows_exporter) | Keine direkte Zuordnung; manuell pruefen | [docs/DESKTOP_LAUNCHER_AND_METRICS_CONTRACT.md](DESKTOP_LAUNCHER_AND_METRICS_CONTRACT.md) |
| [prometheus-operator/prometheus-operator](https://github.com/prometheus-operator/prometheus-operator) | Keine direkte Zuordnung; manuell pruefen | [docs/MODEL_ROUTING_EXPORT_AND_MONITORING.md](MODEL_ROUTING_EXPORT_AND_MONITORING.md) |
| [prometheus/alertmanager](https://github.com/prometheus/alertmanager) | Keine direkte Zuordnung; manuell pruefen | [docs/NATIVE_OPERATIONS_HANDBOOK.md](NATIVE_OPERATIONS_HANDBOOK.md) |
| [prometheus/blackbox_exporter](https://github.com/prometheus/blackbox_exporter) | Keine direkte Zuordnung; manuell pruefen | [docs/ARCHITECTURE_REVIEW_2026-10-25.md](ARCHITECTURE_REVIEW_2026-10-25.md) |
| [prometheus/node_exporter](https://github.com/prometheus/node_exporter) | Menue: Node_Exporter; Registry: node_exporter | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/NODE_EXPORTER_INSTALLATION_NOTES.md](NODE_EXPORTER_INSTALLATION_NOTES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [prometheus/prometheus](https://github.com/prometheus/prometheus) | Menue: Prometheus; Registry: prometheus | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md) |
| [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | Menue: Promptfoo; Registry: promptfoo | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/PROMPTFOO_INSTALLATION_NOTES.md](PROMPTFOO_INSTALLATION_NOTES.md), [docs/SETUP_REVIEW_2026_NEXT_ACTIONS.md](SETUP_REVIEW_2026_NEXT_ACTIONS.md) |
| [protocolbuffers/protobuf](https://github.com/protocolbuffers/protobuf) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [psf/black](https://github.com/psf/black) | Registry: black | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/dev-quality.md](tools/dev-quality.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [psf/requests](https://github.com/psf/requests) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/grok-development-tooling.md](tutorials/grok-development-tooling.md) |
| [puppeteer/puppeteer](https://github.com/puppeteer/puppeteer) | Registry: puppeteer | [docs/PUPPETEER_INSTALLATION_NOTES.md](PUPPETEER_INSTALLATION_NOTES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [py-pdf/pypdf](https://github.com/py-pdf/pypdf) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [pyannote/pyannote-audio](https://github.com/pyannote/pyannote-audio) | Registry: pyannote_audio | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_DEEPFAKE_REVIEW.md](media_studio/AUDIO_DEEPFAKE_REVIEW.md) |
| [pyca/cryptography](https://github.com/pyca/cryptography) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [pydantic/pydantic](https://github.com/pydantic/pydantic) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md), [docs/tutorials/grok-development-tooling.md](tutorials/grok-development-tooling.md) |
| [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/grok-development-tooling.md](tutorials/grok-development-tooling.md) |
| [pydantic/pydantic-settings](https://github.com/pydantic/pydantic-settings) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/grok-development-tooling.md](tutorials/grok-development-tooling.md) |
| [pymupdf/pymupdf](https://github.com/pymupdf/pymupdf) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [pyocd/pyocd](https://github.com/pyocd/pyocd) | Keine direkte Zuordnung; manuell pruefen | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/tools/embedded-debug-hil.md](tools/embedded-debug-hil.md) |
| [pypa/packaging.python.org](https://github.com/pypa/packaging.python.org) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/manus-development-sources.md](tutorials/manus-development-sources.md) |
| [pypa/pip](https://github.com/pypa/pip) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/manus-development-sources.md](tutorials/manus-development-sources.md), [docs/tutorials/manus-development-workflow.md](tutorials/manus-development-workflow.md) |
| [pytest-dev/pytest](https://github.com/pytest-dev/pytest) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/claude-development-tooling.md](tutorials/claude-development-tooling.md), [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [pytest-dev/pytest-cov](https://github.com/pytest-dev/pytest-cov) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [python-arq/arq](https://github.com/python-arq/arq) | Registry: arq | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/arq.md](tools/registry/arq.md) |
| [python-markdown/markdown](https://github.com/python-markdown/markdown) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/markdown-docs-server.md](tools/markdown-docs-server.md) |
| [python-openxml/python-docx](https://github.com/python-openxml/python-docx) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [python-pillow/pillow](https://github.com/python-pillow/pillow) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [python/cpython](https://github.com/python/cpython) | Menue: FinRAG; Menue: FinRobot | [docs/FINRAG_INSTALLATION_NOTES.md](FINRAG_INSTALLATION_NOTES.md), [docs/FINROBOT_INSTALLATION_NOTES.md](FINROBOT_INSTALLATION_NOTES.md), [docs/tools/stable-audio-open.md](tools/stable-audio-open.md) |
| [python/mypy](https://github.com/python/mypy) | Registry: mypy | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/dev-quality.md](tools/dev-quality.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [pytorch/pytorch](https://github.com/pytorch/pytorch) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md), [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [pytorch/torchcodec](https://github.com/pytorch/torchcodec) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/pyannote-audio.md](tools/pyannote-audio.md) |
| [qdrant/qdrant](https://github.com/qdrant/qdrant) | Menue: Qdrant; Registry: qdrant | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/GITOPS_SMALL_VPS.md](GITOPS_SMALL_VPS.md) |
| [qwenlm/qwen-code](https://github.com/qwenlm/qwen-code) | Menue: Qwen_Desktop_Build; Menue: Qwen_Desktop_Study; Registry: qwen_code; Registry: qwen_desktop; Registry: qwen_desktop_build; Registry: qwen_desktop_study | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/agents/CODING_AGENT_INVENTORY.md](agents/CODING_AGENT_INVENTORY.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [qwenlm/qwen3](https://github.com/qwenlm/qwen3) | Menue: Qwen3_235B_A22B; Registry: qwen3_235b | [docs/tools/qwen3-235b.md](tools/qwen3-235b.md) |
| [qwenlm/qwen3-coder](https://github.com/qwenlm/qwen3-coder) | Menue: Qwen_Coder; Registry: qwen_coder | [docs/models/README.md](models/README.md), [docs/tools/qwen-coder.md](tools/qwen-coder.md) |
| [qwenlm/qwen3-tts](https://github.com/qwenlm/qwen3-tts) | Registry: qwen3_tts | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_VIDEO_TOOL_CATALOG.md](media_studio/AUDIO_VIDEO_TOOL_CATALOG.md), [docs/tools/qwen3-tts.md](tools/qwen3-tts.md) |
| [qwenlm/qwq](https://github.com/qwenlm/qwq) | Menue: QwQ_32B; Registry: qwq_32b | [docs/tools/qwq-32b.md](tools/qwq-32b.md) |
| [rabbitmq/rabbitmq-server](https://github.com/rabbitmq/rabbitmq-server) | Registry: rabbitmq | [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/rabbitmq.md](tools/registry/rabbitmq.md) |
| [raffiihza/free-llm-coding-credits](https://github.com/raffiihza/free-llm-coding-credits) | Keine direkte Zuordnung; manuell pruefen | [docs/_API-Keys/FREE_TIERS_AND_TRIAL_CREDITS.md](_API-Keys/FREE_TIERS_AND_TRIAL_CREDITS.md), [docs/_API-Keys/reviews/2026-10-21.md](_API-Keys/reviews/2026-10-21.md), [docs/_API-Keys/reviews/2026-10-26.md](_API-Keys/reviews/2026-10-26.md) |
| [ray-project/llmperf](https://github.com/ray-project/llmperf) | Keine direkte Zuordnung; manuell pruefen | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| [rclone/rclone](https://github.com/rclone/rclone) | Registry: rclone | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md) |
| [react/react](https://github.com/react/react) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md), [docs/tutorials/manus-development-sources.md](tutorials/manus-development-sources.md), [docs/tutorials/manus-development-workflow.md](tutorials/manus-development-workflow.md) |
| [redis/redis](https://github.com/redis/redis) | Registry: redis | [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/redis.md](tools/registry/redis.md) |
| [reflex-dev/reflex](https://github.com/reflex-dev/reflex) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | Menue: Remotion; Registry: remotion | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/openmontage.md](tools/openmontage.md), [docs/tools/remotion.md](tools/remotion.md) |
| [renovatebot/renovate](https://github.com/renovatebot/renovate) | Registry: renovate | [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/audit/MISSING_TOOLS.md](audit/MISSING_TOOLS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [restic/restic](https://github.com/restic/restic) | Registry: restic | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md) |
| [rhasspy/piper](https://github.com/rhasspy/piper) | Registry: piper | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/TOOL_MATRIX.md](TOOL_MATRIX.md) |
| [rhasspy/rhasspy](https://github.com/rhasspy/rhasspy) | Menue: Rhasspy; Registry: rhasspy | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/legacy/rhasspy2/BUILD_REVIEW.md](legacy/rhasspy2/BUILD_REVIEW.md) |
| [rhasspy/wyoming](https://github.com/rhasspy/wyoming) | Menue: Wyoming; Registry: wyoming | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/wyoming.md](tools/registry/wyoming.md) |
| [rhasspy/wyoming-satellite](https://github.com/rhasspy/wyoming-satellite) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/rhasspy-options.md](tools/rhasspy-options.md) |
| [rikorose/deepfilternet](https://github.com/rikorose/deepfilternet) | Registry: deepfilternet | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_DEEPFAKE_REVIEW.md](media_studio/AUDIO_DEEPFAKE_REVIEW.md) |
| [roundcube/roundcubemail](https://github.com/roundcube/roundcubemail) | Registry: roundcube | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/roundcube.md](tools/registry/roundcube.md) |
| [rq/rq](https://github.com/rq/rq) | Registry: queue_manager; Registry: rq | [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [rspamd/rspamd](https://github.com/rspamd/rspamd) | Registry: rspamd | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/rspamd.md](tools/registry/rspamd.md) |
| [rudrabha/wav2lip](https://github.com/rudrabha/wav2lip) | Registry: wav2lip | [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/wav2lip.md](tools/registry/wav2lip.md) |
| [run-llama/llama_index](https://github.com/run-llama/llama_index) | Registry: llamaindex | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/SETUP_REVIEW_2026_NEXT_ACTIONS.md](SETUP_REVIEW_2026_NEXT_ACTIONS.md) |
| [rust-lang/api-guidelines](https://github.com/rust-lang/api-guidelines) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/qwen-development-tooling.md](tutorials/qwen-development-tooling.md) |
| [rust-lang/cargo](https://github.com/rust-lang/cargo) | 62er-Katalog: cargo | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [rust-lang/rust](https://github.com/rust-lang/rust) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/claude-development-tooling.md](tutorials/claude-development-tooling.md), [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [rust-lang/rust-analyzer](https://github.com/rust-lang/rust-analyzer) | 62er-Katalog: rust_analyzer | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/manus-language-infrastructure-sources.md](tutorials/manus-language-infrastructure-sources.md) |
| [rust-lang/rust-clippy](https://github.com/rust-lang/rust-clippy) | 62er-Katalog: clippy | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [rust-lang/rustfmt](https://github.com/rust-lang/rustfmt) | 62er-Katalog: rustfmt | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/manus-language-infrastructure-sources.md](tutorials/manus-language-infrastructure-sources.md) |
| [rust-lang/rustup](https://github.com/rust-lang/rustup) | 62er-Katalog: rustup | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/claude-development-tooling.md](tutorials/claude-development-tooling.md) |
| [ruvnet/ruflo](https://github.com/ruvnet/ruflo) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/ruflo.md](tools/ruflo.md) |
| [rvc-project/retrieval-based-voice-conversion-webui](https://github.com/rvc-project/retrieval-based-voice-conversion-webui) | Menue: RVC; Registry: rvc | [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_DEEPFAKE_REVIEW.md](media_studio/AUDIO_DEEPFAKE_REVIEW.md) |
| [scanny/python-pptx](https://github.com/scanny/python-pptx) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md), [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [scipy/scipy](https://github.com/scipy/scipy) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [sczhou/propainter](https://github.com/sczhou/propainter) | Registry: propainter | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_VIDEO_TOOL_CATALOG.md](media_studio/AUDIO_VIDEO_TOOL_CATALOG.md) |
| [seadve/mousai](https://github.com/seadve/mousai) | Menue: Mousai; Registry: mousai | [docs/AUDIO_RECOGNITION_AND_DOMAIN_MODELS.md](AUDIO_RECOGNITION_AND_DOMAIN_MODELS.md), [docs/tools/mousai.md](tools/mousai.md) |
| [searxng/searxng](https://github.com/searxng/searxng) | Menue: SearXNG; Registry: searxng | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/searxng.md](tools/searxng.md) |
| [semgrep/semgrep](https://github.com/semgrep/semgrep) | Menue: Semgrep; Registry: semgrep | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/MISSING_TOOLS.md](audit/MISSING_TOOLS.md) |
| [serde-rs/serde](https://github.com/serde-rs/serde) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [sfztools/sfizz](https://github.com/sfztools/sfizz) | Registry: sfizz | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_VIDEO_TOOL_CATALOG.md](media_studio/AUDIO_VIDEO_TOOL_CATALOG.md) |
| [sfztools/sfizz-ui](https://github.com/sfztools/sfizz-ui) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/sfizz.md](tools/sfizz.md) |
| [sgl-project/sglang](https://github.com/sgl-project/sglang) | Keine direkte Zuordnung; manuell pruefen | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md), [docs/tutorials/grok-development-tooling.md](tutorials/grok-development-tooling.md) |
| [sharkdp/hyperfine](https://github.com/sharkdp/hyperfine) | Registry: hyperfine | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [showlab/kiwi-edit](https://github.com/showlab/kiwi-edit) | Registry: kiwi_edit | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_VIDEO_TOOL_CATALOG.md](media_studio/AUDIO_VIDEO_TOOL_CATALOG.md) |
| [significant-gravitas/autogpt](https://github.com/significant-gravitas/autogpt) | Menue: AutoGPT; Registry: autogpt | [docs/DOCKER_REMAINDER_2026-10-27.md](DOCKER_REMAINDER_2026-10-27.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/TOOL_INDEX.md](TOOL_INDEX.md) |
| [sigstore/cosign](https://github.com/sigstore/cosign) | Registry: cosign | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md), [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md), [docs/audit/MISSING_TOOLS.md](audit/MISSING_TOOLS.md) |
| [sigstore/policy-controller](https://github.com/sigstore/policy-controller) | Keine direkte Zuordnung; manuell pruefen | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| [siriknikita/openforge](https://github.com/siriknikita/openforge) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/gitlab-openforge-mlflow.md](tools/gitlab-openforge-mlflow.md) |
| [skylot/jadx](https://github.com/skylot/jadx) | Registry: jadx | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/jadx.md](tools/registry/jadx.md) |
| [skyworkai/skyreels-a1](https://github.com/skyworkai/skyreels-a1) | Registry: skyreels_a1 | [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/VIDEO_AVATAR_SYSTEMS.md](VIDEO_AVATAR_SYSTEMS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [slvdev/esp32-ai](https://github.com/slvdev/esp32-ai) | Keine direkte Zuordnung; manuell pruefen | [docs/research/ESP32_AI_LINUX_AND_OLLAMA.md](research/ESP32_AI_LINUX_AND_OLLAMA.md) |
| [snap-research/panda-70m](https://github.com/snap-research/panda-70m) | Keine direkte Zuordnung; manuell pruefen | [docs/media_studio/VIDEO_TRAINING_DATASETS.md](media_studio/VIDEO_TRAINING_DATASETS.md) |
| [sparkaudio/spark-tts](https://github.com/sparkaudio/spark-tts) | Registry: spark_tts | [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/spark_tts.md](tools/registry/spark_tts.md) |
| [spf13/cobra](https://github.com/spf13/cobra) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md), [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [spotify/basic-pitch](https://github.com/spotify/basic-pitch) | Registry: basic_pitch | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_VIDEO_TOOL_CATALOG.md](media_studio/AUDIO_VIDEO_TOOL_CATALOG.md) |
| [sqlalchemy/alembic](https://github.com/sqlalchemy/alembic) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [sqlalchemy/sqlalchemy](https://github.com/sqlalchemy/sqlalchemy) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md), [docs/tutorials/grok-development-tooling.md](tutorials/grok-development-tooling.md) |
| [sqlfluff/sqlfluff](https://github.com/sqlfluff/sqlfluff) | 62er-Katalog: sqlfluff; Registry: sqlfluff | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md) |
| [sqlite/sqlite](https://github.com/sqlite/sqlite) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/claude-development-tooling.md](tutorials/claude-development-tooling.md), [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [squidfunk/mkdocs-material](https://github.com/squidfunk/mkdocs-material) | Keine direkte Zuordnung; manuell pruefen | [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md) |
| [sst/opencode](https://github.com/sst/opencode) | Keine direkte Zuordnung; manuell pruefen | [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md) |
| [stability-ai/stable-audio-tools](https://github.com/stability-ai/stable-audio-tools) | Registry: stable_audio_open | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_VIDEO_TOOL_CATALOG.md](media_studio/AUDIO_VIDEO_TOOL_CATALOG.md) |
| [stackrox/kube-linter](https://github.com/stackrox/kube-linter) | 62er-Katalog: kubelinter; Registry: kubelinter | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md) |
| [stakira/openutau](https://github.com/stakira/openutau) | Keine direkte Zuordnung; manuell pruefen | [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [stalwartlabs/stalwart](https://github.com/stalwartlabs/stalwart) | Registry: sieve; Registry: stalwart; Registry: stalwart_mail | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/TOOL_INDEX.md](TOOL_INDEX.md) |
| [statsmodels/statsmodels](https://github.com/statsmodels/statsmodels) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [stirling-tools/stirling-pdf](https://github.com/stirling-tools/stirling-pdf) | Menue: Stirling_PDF; Registry: stirling_pdf | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md) |
| [streamlit/streamlit](https://github.com/streamlit/streamlit) | Menue: Streamlit; Registry: streamlit | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/github-gap-tools.md](tools/github-gap-tools.md), [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [subtitleedit/subtitleedit](https://github.com/subtitleedit/subtitleedit) | Registry: subtitleedit | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/subtitleedit.md](tools/registry/subtitleedit.md) |
| [supabase/supabase](https://github.com/supabase/supabase) | Menue: Supabase; Registry: supabase; Registry: supabase_self_hosted | [docs/DOCKER_REMAINDER_2026-10-27.md](DOCKER_REMAINDER_2026-10-27.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/supabase_self_hosted.md](tools/registry/supabase_self_hosted.md) |
| [supervisor/supervisor](https://github.com/supervisor/supervisor) | Registry: supervisord | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/supervisord.md](tools/registry/supervisord.md) |
| [sveltejs/svelte](https://github.com/sveltejs/svelte) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [swatinem/rust-cache](https://github.com/swatinem/rust-cache) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [swe-agent/swe-agent](https://github.com/swe-agent/swe-agent) | Registry: swe_agent | [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/swe_agent.md](tools/registry/swe_agent.md) |
| [syncthing/syncthing](https://github.com/syncthing/syncthing) | Menue: Syncthing; Registry: syncthing | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/SETUP_REVIEW_2026_NEXT_ACTIONS.md](SETUP_REVIEW_2026_NEXT_ACTIONS.md) |
| [systemd/systemd](https://github.com/systemd/systemd) | Registry: systemd_user_units | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/systemd_user_units.md](tools/registry/systemd_user_units.md) |
| [systran/faster-whisper](https://github.com/systran/faster-whisper) | Menue: Faster_Whisper; Registry: faster_whisper | [docs/GITHUB_TOOL_CANDIDATES_REVIEW.md](GITHUB_TOOL_CANDIDATES_REVIEW.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/reviews/2026-10-26-platform-patch-plan.md](reviews/2026-10-26-platform-patch-plan.md) |
| [tailscale/tailscale](https://github.com/tailscale/tailscale) | Keine direkte Zuordnung; manuell pruefen | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| [tailwindlabs/tailwindcss](https://github.com/tailwindlabs/tailwindcss) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [tale/headplane](https://github.com/tale/headplane) | Registry: headplane | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/headplane.md](tools/registry/headplane.md) |
| [tashfeenahmed/freellmapi](https://github.com/tashfeenahmed/freellmapi) | Registry: freellmapi | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/_API-Keys/API_KEY_GUIDE.md](_API-Keys/API_KEY_GUIDE.md), [docs/_API-Keys/FREE_TIERS_AND_TRIAL_CREDITS.md](_API-Keys/FREE_TIERS_AND_TRIAL_CREDITS.md) |
| [taskforcesh/bullmq](https://github.com/taskforcesh/bullmq) | Registry: bullmq | [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [tauri-apps/tauri](https://github.com/tauri-apps/tauri) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [tcort/markdown-link-check](https://github.com/tcort/markdown-link-check) | Keine direkte Zuordnung; manuell pruefen | [docs/quality/EXTERNAL_LINK_POLICY.md](quality/EXTERNAL_LINK_POLICY.md) |
| [temporalio/temporal](https://github.com/temporalio/temporal) | Registry: temporal | [docs/audit/MISSING_TOOLS.md](audit/MISSING_TOOLS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/native-go-controllers.md](tools/native-go-controllers.md) |
| [tencent-hunyuan/hunyuan3d-2.1](https://github.com/tencent-hunyuan/hunyuan3d-2.1) | Keine direkte Zuordnung; manuell pruefen | [docs/AI_3D_STUDIO.md](AI_3D_STUDIO.md) |
| [tencent-hunyuan/hunyuanvideo](https://github.com/tencent-hunyuan/hunyuanvideo) | Keine direkte Zuordnung; manuell pruefen | [docs/media_studio/VIDEO_TRAINING_DATASETS.md](media_studio/VIDEO_TRAINING_DATASETS.md) |
| [tencentarc/gfpgan](https://github.com/tencentarc/gfpgan) | Menue: GFPGAN; Registry: gfpgan | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/gfpgan.md](tools/registry/gfpgan.md) |
| [terraform-aws-modules/terraform-aws-vpc](https://github.com/terraform-aws-modules/terraform-aws-vpc) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/qwen-development-tooling.md](tutorials/qwen-development-tooling.md) |
| [terraform-docs/terraform-docs](https://github.com/terraform-docs/terraform-docs) | 62er-Katalog: terraform_docs; Registry: terraform_docs | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md) |
| [terraform-linters/tflint](https://github.com/terraform-linters/tflint) | 62er-Katalog: tflint; Registry: tflint | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md) |
| [tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract) | Registry: tesseract | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/personnel-documents.md](tools/personnel-documents.md) |
| [testcontainers/testcontainers-go](https://github.com/testcontainers/testcontainers-go) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [testcontainers/testcontainers-python](https://github.com/testcontainers/testcontainers-python) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [testssl/testssl.sh](https://github.com/testssl/testssl.sh) | Registry: testssl | [docs/tools/native-security-candidates.md](tools/native-security-candidates.md) |
| [the-djmaze/snappymail](https://github.com/the-djmaze/snappymail) | Registry: snappymail | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/snappymail.md](tools/registry/snappymail.md) |
| [theory/pgtap](https://github.com/theory/pgtap) | 62er-Katalog: pgtap | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/manus-language-infrastructure-sources.md](tutorials/manus-language-infrastructure-sources.md) |
| [thudm/cogvideo](https://github.com/thudm/cogvideo) | Menue: CogVideoX; Registry: cogvideox | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/github-gap-tools.md](tools/github-gap-tools.md) |
| [till-schaefer/jarvis](https://github.com/till-schaefer/jarvis) | Keine direkte Zuordnung; manuell pruefen | [docs/quality/EXTERNAL_LINK_POLICY.md](quality/EXTERNAL_LINK_POLICY.md), [docs/tools/jarvis-hermes-dashboard.md](tools/jarvis-hermes-dashboard.md) |
| [tmc/langchaingo](https://github.com/tmc/langchaingo) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [tmelyralab/musetalk](https://github.com/tmelyralab/musetalk) | Menue: MuseTalk; Registry: musetalk | [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/VIDEO_AVATAR_SYSTEMS.md](VIDEO_AVATAR_SYSTEMS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [tmux/tmux](https://github.com/tmux/tmux) | Registry: tmux | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/tmux.md](tools/registry/tmux.md) |
| [tokio-rs/axum](https://github.com/tokio-rs/axum) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md), [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [tokio-rs/tokio](https://github.com/tokio-rs/tokio) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md), [docs/tutorials/perplexity-development-tooling.md](tutorials/perplexity-development-tooling.md) |
| [traefik/traefik](https://github.com/traefik/traefik) | Menue: Traefik; Registry: traefik | [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [trepan-debuggers/bashdb](https://github.com/trepan-debuggers/bashdb) | 62er-Katalog: bashdb | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/quality/EXTERNAL_LINK_POLICY.md](quality/EXTERNAL_LINK_POLICY.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md) |
| [trufflesecurity/trufflehog](https://github.com/trufflesecurity/trufflehog) | Registry: trufflehog | [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/native-security-candidates.md](tools/native-security-candidates.md) |
| [trusteddomainproject/opendkim](https://github.com/trusteddomainproject/opendkim) | Registry: opendkim | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/opendkim.md](tools/registry/opendkim.md) |
| [trusteddomainproject/opendmarc](https://github.com/trusteddomainproject/opendmarc) | Registry: opendmarc | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/opendmarc.md](tools/registry/opendmarc.md) |
| [typesettingtools/aegisub](https://github.com/typesettingtools/aegisub) | Registry: aegisub | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/AUDIO_VIDEO_TOOL_CATALOG.md](media_studio/AUDIO_VIDEO_TOOL_CATALOG.md) |
| [unitech/pm2](https://github.com/unitech/pm2) | Registry: pm2 | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/pm2.md](tools/registry/pm2.md) |
| [unity-technologies/ml-agents](https://github.com/unity-technologies/ml-agents) | Keine direkte Zuordnung; manuell pruefen | [docs/tools/ai-game-engines-xr-wallpaper.md](tools/ai-game-engines-xr-wallpaper.md) |
| [unslothai/unsloth](https://github.com/unslothai/unsloth) | Menue: Unsloth | [docs/Profil/LLM-Builder.doc.md](Profil/LLM-Builder.doc.md) |
| [unstructured-io/unstructured](https://github.com/unstructured-io/unstructured) | Menue: Unstructured; Registry: unstructured | [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/unstructured.md](tools/registry/unstructured.md) |
| [username/huginn](https://github.com/username/huginn) | Keine direkte Zuordnung; manuell pruefen | [docs/HUGINN_REPO_REF_GUIDE.md](HUGINN_REPO_REF_GUIDE.md), [docs/quality/EXTERNAL_LINK_POLICY.md](quality/EXTERNAL_LINK_POLICY.md) |
| [valkey-io/valkey](https://github.com/valkey-io/valkey) | Registry: valkey | [docs/tools/valkey.md](tools/valkey.md) |
| [vast-ai-research/comfyui-tripo](https://github.com/vast-ai-research/comfyui-tripo) | Keine direkte Zuordnung; manuell pruefen | [docs/AI_3D_STUDIO.md](AI_3D_STUDIO.md) |
| [vast-ai-research/triposr](https://github.com/vast-ai-research/triposr) | Keine direkte Zuordnung; manuell pruefen | [docs/AI_3D_STUDIO.md](AI_3D_STUDIO.md) |
| [vega/altair](https://github.com/vega/altair) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/meta-development-tooling.md](tutorials/meta-development-tooling.md) |
| [velero-io/velero](https://github.com/velero-io/velero) | Menue: Velero; Registry: velero | [docs/VELERO_INSTALLATION_NOTES.md](VELERO_INSTALLATION_NOTES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | Registry: find_skills | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [vercel/next.js](https://github.com/vercel/next.js) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [vibrantlabsai/ragas](https://github.com/vibrantlabsai/ragas) | Registry: ragas | [docs/tools/python-reviewed-native.md](tools/python-reviewed-native.md) |
| [vishakhpk/creative-instructions](https://github.com/vishakhpk/creative-instructions) | Menue: CoPoet; Registry: copoet | [docs/MUSIC_LYRICS_MODEL_CATALOG.md](MUSIC_LYRICS_MODEL_CATALOG.md), [docs/tools/copoet.md](tools/copoet.md) |
| [visualbruno/comfyui-hunyuan3d-2-1](https://github.com/visualbruno/comfyui-hunyuan3d-2-1) | Keine direkte Zuordnung; manuell pruefen | [docs/AI_3D_STUDIO.md](AI_3D_STUDIO.md) |
| [vitejs/vite](https://github.com/vitejs/vite) | 62er-Katalog: vite | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [vitest-dev/vitest](https://github.com/vitest-dev/vitest) | 62er-Katalog: vitest | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md), [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [vladmandic/sdnext](https://github.com/vladmandic/sdnext) | Registry: sdnext | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/SOCIAL_AVATAR_AUTOMATION.md](media_studio/SOCIAL_AVATAR_AUTOMATION.md), [docs/tools/sdnext.md](tools/sdnext.md) |
| [vllm-project/vllm](https://github.com/vllm-project/vllm) | Registry: vllm | [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md), [docs/TOOLS_CATALOG.md](TOOLS_CATALOG.md), [docs/architecture/ENTERPRISE_HARDENING_ROADMAP.md](architecture/ENTERPRISE_HARDENING_ROADMAP.md) |
| [vmware-tanzu/velero](https://github.com/vmware-tanzu/velero) | Keine direkte Zuordnung; manuell pruefen | [docs/PLATFORM_GAP_IMPLEMENTATION_2026-10-27.md](PLATFORM_GAP_IMPLEMENTATION_2026-10-27.md), [docs/SETUP_REVIEW_2026_CODEX.md](SETUP_REVIEW_2026_CODEX.md) |
| [vscodium/vscodium](https://github.com/vscodium/vscodium) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md) |
| [vuejs/core](https://github.com/vuejs/core) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/chatgpt-tooling-sources.md](tutorials/chatgpt-tooling-sources.md), [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [wan-video/wan2.1](https://github.com/wan-video/wan2.1) | Registry: wan21 | [docs/Profile/OpenHiggsStack_AI_Cinema_Studio.md](Profile/OpenHiggsStack_AI_Cinema_Studio.md), [docs/Profile/Video_Generation_ComfyUI_Wan.md](Profile/Video_Generation_ComfyUI_Wan.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [wan-video/wan2.2](https://github.com/wan-video/wan2.2) | Keine direkte Zuordnung; manuell pruefen | [docs/Profile/OpenHiggsStack_AI_Cinema_Studio.md](Profile/OpenHiggsStack_AI_Cinema_Studio.md), [docs/Profile/Video_Generation_ComfyUI_Wan.md](Profile/Video_Generation_ComfyUI_Wan.md), [docs/models/SONGSAGE_MIDI_RESEARCH.md](models/SONGSAGE_MIDI_RESEARCH.md) |
| [wazuh/wazuh](https://github.com/wazuh/wazuh) | Registry: wazuh | [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/wazuh.md](tools/registry/wazuh.md) |
| [weaviate/weaviate](https://github.com/weaviate/weaviate) | Menue: Weaviate; Registry: weaviate | [docs/DOCKER_TO_GITHUB.md](DOCKER_TO_GITHUB.md), [docs/RECOMMENDED_TOOLS.md](RECOMMENDED_TOOLS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [webpack/webpack](https://github.com/webpack/webpack) | Keine direkte Zuordnung; manuell pruefen | [docs/tutorials/gemini-development-tooling.md](tutorials/gemini-development-tooling.md) |
| [windmill-labs/windmill](https://github.com/windmill-labs/windmill) | Registry: windmill | [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/media_studio/SOCIAL_AVATAR_AUTOMATION.md](media_studio/SOCIAL_AVATAR_AUTOMATION.md) |
| [withastro/astro](https://github.com/withastro/astro) | Registry: websitefactory | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md) |
| [worldveil/dejavu](https://github.com/worldveil/dejavu) | Menue: Dejavu; Registry: dejavu | [docs/AUDIO_RECOGNITION_AND_DOMAIN_MODELS.md](AUDIO_RECOGNITION_AND_DOMAIN_MODELS.md), [docs/tools/SOURCE_INSTALL_READINESS.md](tools/SOURCE_INSTALL_READINESS.md), [docs/tools/dejavu.md](tools/dejavu.md) |
| [xerj-org/xerj](https://github.com/xerj-org/xerj) | Registry: xerj | [docs/tools/xerj.md](tools/xerj.md) |
| [xinntao/real-esrgan](https://github.com/xinntao/real-esrgan) | Menue: RealESRGAN; Registry: realesrgan | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/realesrgan.md](tools/registry/realesrgan.md) |
| [yannh/kubeconform](https://github.com/yannh/kubeconform) | 62er-Katalog: kubeconform; Registry: kubeconform | [docs/DEVELOPMENT_TOOLS_OVERVIEW.md](DEVELOPMENT_TOOLS_OVERVIEW.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/sources/2026-10-24/language-infrastructure.md](sources/2026-10-24/language-infrastructure.md) |
| [yl4579/styletts2](https://github.com/yl4579/styletts2) | Registry: styletts2 | [docs/TOOL_MATRIX.md](TOOL_MATRIX.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/styletts2.md](tools/registry/styletts2.md) |
| [yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp) | Keine direkte Zuordnung; manuell pruefen | [docs/TOOL_GAP_ANALYSIS.md](TOOL_GAP_ANALYSIS.md) |
| [zai-org/cogvideo](https://github.com/zai-org/cogvideo) | Keine direkte Zuordnung; manuell pruefen | [docs/media_studio/SOCIAL_AVATAR_AUTOMATION.md](media_studio/SOCIAL_AVATAR_AUTOMATION.md), [docs/media_studio/VIDEO_TRAINING_DATASETS.md](media_studio/VIDEO_TRAINING_DATASETS.md) |
| [zai-org/glm-5](https://github.com/zai-org/glm-5) | Keine direkte Zuordnung; manuell pruefen | [docs/media_studio/HYBRID_MODELS_AND_WAN.md](media_studio/HYBRID_MODELS_AND_WAN.md) |
| [zaproxy/zaproxy](https://github.com/zaproxy/zaproxy) | Registry: owasp_zap | [docs/tools/security-data-native.md](tools/security-data-native.md) |
| [zeek/zeek](https://github.com/zeek/zeek) | Registry: zeek | [docs/GITHUB_TOOL_SOURCES.md](GITHUB_TOOL_SOURCES.md), [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/zeek.md](tools/registry/zeek.md) |
| [zhanqu945/poetone](https://github.com/zhanqu945/poetone) | Menue: PoeTone; Registry: poetone | [docs/MUSIC_LYRICS_MODEL_CATALOG.md](MUSIC_LYRICS_MODEL_CATALOG.md), [docs/tools/poetone.md](tools/poetone.md) |
| [zotero/zotero](https://github.com/zotero/zotero) | Registry: zotero | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/zotero.md](tools/registry/zotero.md) |
| [zx2c4/password-store](https://github.com/zx2c4/password-store) | Registry: pass | [docs/audit/TOOL_INVENTORY.md](audit/TOOL_INVENTORY.md), [docs/tools/registry/pass.md](tools/registry/pass.md) |

## Strukturfehler

Doppelte Registry-IDs: keine

Doppelte Menue-Keys: keine

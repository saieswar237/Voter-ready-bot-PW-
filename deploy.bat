@echo off
"C:\Users\Sai\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" run deploy voter-ready-bot --source . --region asia-south1 --allow-unauthenticated --update-env-vars GEMINI_API_KEY=AIzaSyAp811tCdnOwH_u3FlP0TfC5WajufMcA_Y --quiet

### Deployment

Currently, the app is deployed on a compute engine on GCP.

The app can be found in `/home/fahyik/upsailai-demo`.

To deploy new code :
- Make sure you are on branch `feature/server`.
- Do a `git pull` to fetch updated code
- Restart `sudo supervisorctl restart fastapi`


Create new virtual environment

```bash
python –m venv .venv
```
Activate the virtual environment (Using PowerShell)

```bash
.venv\Scripts\Activate.ps1
```
Install dependences

```bash
pip install -r .\requirements.txt
```
First train model

```bash
rasa train
```
Waiting for training finish...

Run rasa server
```bash
rasa run -m models --enable-api --cors "*"
```

Open new terminal in this direction and activate virtual environment

Run actions server

```bash
rasa run actions
```

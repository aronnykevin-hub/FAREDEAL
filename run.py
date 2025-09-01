import os
from supermarket_app import create_app
from supermarket_app.seed import seed

app = create_app()
seed(app)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)

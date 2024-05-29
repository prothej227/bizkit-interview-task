from phasebook import create_app

app = create_app()
app.json.sort_keys = False

if __name__ == "__main__":
    app.run(debug=True)
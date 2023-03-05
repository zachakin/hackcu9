from flask import Flask, render_template, url_for, request, redirect, session
from helpers import link_to_file, file_to_text, chatbot
from keys import MY_SECRET

app = Flask(__name__)
app.secret_key = MY_SECRET

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            if link_to_file(request.form['content'],'static/db/temp'):
                message = "Summarize this YouTube video: " + file_to_text('static/db/temp.mp3')
                tmp = {"role": "user", "content": message}
                session['messages'] = [ tmp ]
                return redirect('/chat')
            else:
                return redirect('/')
        except:
            return redirect('/')

    else:
        return render_template('index.html')

@app.route('/chat', methods=['POST', 'GET'])
def chat():
    if request.method == 'POST':
        session['messages'].append({'role':'user', 'content': request.form['content']})

    session['messages'] = chatbot(session['messages'])
    return render_template('chat.html', messages = session['messages'])

if __name__ == "__main__":
    app.run(debug=False, port=5001)
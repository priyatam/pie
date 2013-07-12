from flask import Flask, render_template
import os, sys, re
import os.path, time
from markdown import Markdown
import config
import json

app = Flask(__name__, static_folder="templates/static")
notes_dir = 'notes/'

import yaml
import StringIO

def yaml_extract(text):
    yaml_data = re.search(u"---(.+?)---\n", text, flags=re.U|re.S).group(1)
    return (yaml.load(StringIO.StringIO(yaml_data)), re.sub(u"---(.+?)---\n", "", text, flags=re.U|re.S))


@app.route('/')
def index():
    notes = []
    metas = []
    for note in os.listdir(notes_dir):
        note = notes_dir + note
        ctime = time.ctime(os.path.getmtime(note))
        mtime = time.ctime(os.path.getctime(note))
        text = open(note).read()
        (meta, text) = yaml_extract(text)
        md = Markdown(extensions=['nl2br'], output_format="html5")
        html = md.convert(text)
        metas_dict = { "_name": note, "_ctime": ctime, "_mtime": mtime, "text": text }
        mega_dict = { "_name": note, "_ctime": ctime, "_mtime": mtime, "html": html }
        mega_dict.update(meta)
        metas_dict.update(meta)
        notes.append(mega_dict)
        metas.append(metas_dict)

    notes = sorted(notes, key=lambda e: e['_mtime'], reverse=True)
    metas_json = json.dumps(metas)
    return render_template('index.html', notes=notes, config=config, meta_data=metas_json)

from flask_frozen import Freezer

freezer = Freezer(app)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        app.run(debug=True)
    else:
        freezer.freeze()
        os.system("cp ./build/index.html ./index.html")
        app.run(port=8000)

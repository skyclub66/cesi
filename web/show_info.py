from flask import Flask, render_template, url_for, redirect
from getProcInfo import Config, Connection, Node, CONFIG_FILE
import getProcInfo 
import xmlrpclib

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def showAllProcess():
    node_list = []
    node_names = Config(CONFIG_FILE).getAllNodeNames()
    for node_name in node_names:
        node_name = node_name[5:]
        node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
        node = Node(node_config)
        node_list.append(node)

    for node in node_list:
        for process in node.process_list:
            print node.name, process.name

    return ""
    
@app.route('/node/<node_name>')
def showNode(node_name):
    node = Node(node_name)
    return render_template('show_info.html', process_list = node.process_list, node_name = node_name)

@app.route('/node/<node_name>/process/stop/<process_name>')
def stopProcess(node_name, process_name):
    Node(node_name).connection.supervisor.stopProcess(process_name)
    return redirect(url_for('nodelist', node_name = node_name)) 

@app.route('/node/<node_name>/process/start/<process_name>')
def startProcess(node_name, process_name):
    Node(node_name).connection.supervisor.startProcess(process_name)
    return redirect(url_for('nodelist', node_name = node_name)) 

@app.route('/node/<node_name>/process/restart/<process_name>')
def restartProcess(node_name, process_name):
    Node(node_name).connection.supervisor.stopProcess(process_name)
    Node(node_name).connection.supervisor.startProcess(process_name)
    return redirect(url_for('nodelist', node_name = node_name)) 

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

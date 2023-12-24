from flask import Flask, request, render_template, redirect
import xml.etree.ElementTree as ET

app = Flask(__name__, static_url_path='/static')

# Define the XML file path
xml_file = 'data.xml'

# Function to parse XML and return data
def parse_xml():
    tree = ET.parse(xml_file)
    root = tree.getroot()
    data = []
    for information in root.findall('information'):
        title = information.find('title').text
        content = information.find('content').text
        keyword = information.find('keyword').text
        summary = information.find('summary').text
        data.append({'title': title, 'content': content, 'keyword': keyword, 'summary': summary})
    return data

# Route to display data in the HTML table
@app.route('/', methods=['POST','GET'])
@app.route('/showall', methods=['POST','GET'])
def display_data():
    data = parse_xml()
    return render_template('main.html', data=data)



# SEARCH FUNCTION
@app.route('/search', methods=['POST'])
def search_data():
    search_term = request.form['search_term'].lower()
    data = parse_xml()  # Parse the XML file as you did before
    filtered_data = [item for item in data if search_term in item['title'].lower() or
                                            search_term in item['content'].lower() or
                                            search_term in item['keyword'].lower() or
                                            search_term in item['summary'].lower()]
    return render_template('main.html', data=filtered_data)


#CALLING ADD MODAL FORM
@app.route('/openmodal')
def modal_add_data():
    return render_template('modal-add-data.html', modal_add_data=modal_add_data)

# Function to create an XML structure and append it to an external XML file
def create_xml_structure(title, keyword, summary, content):
    xml_file = 'data.xml'

    # Create an 'information' element
    info_element = ET.Element('information')

    # Create child elements and set their text
    title_element = ET.Element('title')
    title_element.text = title

    keyword_element = ET.Element('keyword')
    keyword_element.text = keyword

    summary_element = ET.Element('summary')
    summary_element.text = summary

    content_element = ET.Element('content')
    content_element.text = content

    # Append the child elements to the 'information' element
    info_element.append(title_element)
    info_element.append(keyword_element)
    info_element.append(summary_element)
    info_element.append(content_element)

    # Parse the existing XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Append the 'information' element to the root of the XML
    root.append(info_element)

    # Write the modified XML back to the file, including the XML declaration
    tree.write(xml_file, xml_declaration=True, encoding='utf-8')
    

# Route to display the form
@app.route('/', methods=['GET'])
def show_form():
    return render_template('modal-add-data.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        title = request.form['title']
        keyword = request.form['keyword']
        summary = request.form['summary']
        content = request.form['content']


    create_xml_structure(title, keyword, summary, content)
    data = parse_xml()
    return render_template('main.html', data=data)


# Route to handle the delete action
@app.route('/delete/<int:index>', methods=['POST'])
def delete_data(index):
    delete_xml_element(index)
    return redirect('/showall')


# Function to delete an XML element by index
def delete_xml_element(index):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    try:
        # Attempt to remove the element at the specified index
        root.remove(root[index])
    except IndexError:
        # Handle the case where the index is out of bounds
        pass

    # Write the modified XML back to the file
    tree.write(xml_file, xml_declaration=True, encoding='utf-8')


#CALLING EDIT MODAL FORM
# Route to handle the edit action (displaying an edit form)
@app.route('/edit/<int:index>', methods=['POST','GET'])
def edit_data(index):
    data = parse_xml()
    item_to_edit = data[index - 1]  # Subtract 1 because index starts from 1 in Jinja2 templates
    return render_template('modal-edit-data.html', item_to_edit=item_to_edit, index=index)

# Route to display the edit form
@app.route('/edit-form', methods=['POST','GET'])
def edit_form():
    index = int(request.form['index'])  # Get the index from the form
    data = parse_xml()
    item_to_edit = data[index - 1]  # Subtract 1 because index starts from 1 in Jinja2 templates
    return render_template('modal-edit-data.html', item_to_edit=item_to_edit, index=index)

# Route to handle the form submission when editing
@app.route('/update/<int:index>', methods=['POST','GET'])
def update_data(index):
    if request.method == 'POST':
        title = request.form['title']
        keyword = request.form['keyword']
        summary = request.form['summary']
        content = request.form['content']

    update_xml_element(index - 1, title, keyword, summary, content)  # Subtract 1 for the index
    data = parse_xml()
    return render_template('main.html', data=data)

# Function to update an XML element by index
def update_xml_element(index, title, keyword, summary, content):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    try:
        # Attempt to update the element at the specified index
        info_element = root[index]
        info_element.find('title').text = title
        info_element.find('keyword').text = keyword
        info_element.find('summary').text = summary
        info_element.find('content').text = content
    except IndexError:
        # Handle the case where the index is out of bounds
        pass

    # Write the modified XML back to the file
    tree.write(xml_file, xml_declaration=True, encoding='utf-8')


if __name__ == '__main__':
    app.run(debug=False) #app.run(debug=True), change to debug
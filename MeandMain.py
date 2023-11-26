from flask import Flask, request, redirect, url_for, render_template, flash
from meandform import ValidationForm, RadioForm
import csv
from MLModel import train_model_RFC, train_model_manual

app = Flask(__name__)
app.config['SECRET_KEY'] = '0cd87b7e35311a0f72e83b5a44cfead6bb5fa11a42362021942438a732f44776'

@app.route('/')
def index():
    return render_template("meandindex.html", Title='index')

@app.route('/form', methods=['POST', 'GET'])
def form():
    def check_user_data(name):
        with open("MLdatafinal.csv", 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if name == row[1]:
                    if row[2] == '0' and row[3] == '0' and row[4] == '0' and row[5] == '0':
                        hasdata = False
                    else: hasdata = True
        return hasdata

    form = ValidationForm()
    if form.validate_on_submit():
        csv_file_user = "meand_users.csv"
        with open(csv_file_user, 'r') as csvfile:
            reader = csv.reader(csvfile)
            user_found = False
            for row in reader:
                if form.name.data == row[1]:
                    user_found = True
                    if form.email.data == row[4]:
                        flash(f'반가워요, {form.name.data}님!', 'success')
                        if check_user_data(form.name.data) == True:
                            return redirect(url_for('results', name=form.name.data))
                        else:
                            return redirect(url_for('getdata', name=form.name.data))
                    else:
                        flash(f'앗, 이메일 주소가 맞지 않는 것 같아요.', 'warning')
            if user_found == False:
                flash(f'앗, 미앤드 회원이 아니신가 봐요. 공식 홈페이지에서 가입을 하고 와주세요!', 'danger')
                render_template("meandform.html", Title='form', form=form)
    return render_template("meandform.html", Title='form', form=form)
    #Debugged with ChatGPT: https://chat.openai.com/share/5730d06f-5b2e-4bcf-ad66-88cbf0b0fe7f

@app.route('/getdata',  methods=['POST', 'GET'])
def getdata():
    form = RadioForm()
    name = request.args.get('name')
    if form.validate_on_submit():
        return redirect(url_for('recommend', name=name, selected_choice = form.choices.data))
    return render_template("meandgetdata.html", Title='getdata', form=form)

@app.route('/results')
def results():
    name = request.args.get('name')

    #Defining some functions that retrieve information from CSV files
    def find_bought_items(name):
        items = []
        csv_file_order = "MLdatafinal.csv"
        with open(csv_file_order, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if name == row[1]:
                    items.append(row[6])
                    items.append(row[7])
                    items.append(row[8])
                    return items
    
    def find_prod_info(prod_no):
        csv_file_order = "meand_items.csv"
        with open(csv_file_order, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if str(prod_no) == row[0]:
                    return row[1], row[2], row[4], row[8], row[9], row[10] #category, name, price, description, image, url

    #Getting prediction result along with shopping history
    result_array = train_model_RFC(name)
    previous_items = find_bought_items(name)

    pred_result_1 = result_array[0]
    pred_result_2 = result_array[1]
    pred_result_3 = result_array[2]

    #Making sure predicted items are not recently bought items
    for result in pred_result_1:
        if result != 0:
            if str(result) not in previous_items:
                predict_item_1 = result
                break
    
    for result in pred_result_2:
        if result != 0:
            if str(result) not in previous_items:
                if result != predict_item_1:
                    predict_item_2 = result
                    break
    
    for result in pred_result_3:
        if result != 0:
            if str(result) not in previous_items:
                if result != predict_item_1:
                    if result != predict_item_2:
                        predict_item_3 = result
                        break
    
    #Defining variables to deliver to html page (recommendations)
    predict_item_1_name = find_prod_info(predict_item_1)[1]
    predict_item_1_category = find_prod_info(predict_item_1)[0]
    predict_item_1_price = find_prod_info(predict_item_1)[2]
    predict_item_1_des = find_prod_info(predict_item_1)[3]
    predict_item_1_img = find_prod_info(predict_item_1)[4]
    predict_item_1_url = find_prod_info(predict_item_1)[5]

    predict_item_2_name = find_prod_info(predict_item_2)[1]
    predict_item_2_category = find_prod_info(predict_item_2)[0]
    predict_item_2_price = find_prod_info(predict_item_2)[2]
    predict_item_2_des = find_prod_info(predict_item_2)[3]
    predict_item_2_img = find_prod_info(predict_item_2)[4]
    predict_item_2_url = find_prod_info(predict_item_2)[5]

    predict_item_3_name = find_prod_info(predict_item_3)[1]
    predict_item_3_category = find_prod_info(predict_item_3)[0]
    predict_item_3_price = find_prod_info(predict_item_3)[2]
    predict_item_3_des = find_prod_info(predict_item_3)[3]
    predict_item_3_img = find_prod_info(predict_item_3)[4]
    predict_item_3_url = find_prod_info(predict_item_3)[5]

    #Defining variables to deliver to html page (previosly shopped)
    if previous_items[0] != '0':
        previous_item_1 = previous_items[0]
        previous_item_1_name = find_prod_info(previous_items[0])[1]
        previous_item_1_category = find_prod_info(previous_items[0])[0]
        previous_item_1_price = find_prod_info(previous_items[0])[2]
        previous_item_1_des = find_prod_info(previous_items[0])[3]
        previous_item_1_img = find_prod_info(previous_items[0])[4]
        previous_item_1_url = find_prod_info(previous_items[0])[5]
    else: previous_item_1 = None

    return render_template("meandresults.html", Title='results',
                            name=name,
                            predict_item_1=predict_item_1,
                            predict_item_2=predict_item_2,
                            predict_item_3=predict_item_3,

                            predict_item_1_name=predict_item_1_name,
                            predict_item_1_category=predict_item_1_category,
                            predict_item_1_status=predict_item_1_category,
                            predict_item_1_price=predict_item_1_price,
                            predict_item_1_des=predict_item_1_des,
                            predict_item_1_img=predict_item_1_img,
                            predict_item_1_url=predict_item_1_url,

                            predict_item_2_name=predict_item_2_name,
                            predict_item_2_category=predict_item_2_category,
                            predict_item_2_status=predict_item_2_category,
                            predict_item_2_price=predict_item_2_price,
                            predict_item_2_des=predict_item_2_des,
                            predict_item_2_img=predict_item_2_img,
                            predict_item_2_url=predict_item_2_url,

                            predict_item_3_name=predict_item_3_name,
                            predict_item_3_category=predict_item_3_category,
                            predict_item_3_status=predict_item_3_category,
                            predict_item_3_price=predict_item_3_price,
                            predict_item_3_des=predict_item_3_des,
                            predict_item_3_img=predict_item_3_img,
                            predict_item_3_url=predict_item_3_url,

                            previous_item_1=previous_item_1,
                            previous_item_1_name=previous_item_1_name,
                            previous_item_1_status=previous_item_1_category,
                            previous_item_1_price=previous_item_1_price,
                            previous_item_1_des=previous_item_1_des,
                            previous_item_1_img=previous_item_1_img,
                            previous_item_1_url=previous_item_1_url
                           )

@app.route('/recommend')
def recommend():

    def find_prod_info(prod_no):
        csv_file_order = "meand_items.csv"
        with open(csv_file_order, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if str(prod_no) == row[0]:
                    return row[1], row[2], row[4], row[8], row[9], row[10] #category, name, price, description, image, url

    name = request.args.get('name')
    category = request.args.get('selected_choice')
    info_list=[]
    if category == 'category11':
        info_list = ['3','0','0','0']
    elif category == 'category13':
        info_list = ['0','3','0','0']
    elif category == 'category14':
        info_list = ['0','0','3','0']
    elif category == 'category15':
        info_list = ['0','0','0','3']

    result_array = train_model_manual(info_list)

    predict_item_1 = result_array[0][0]
    pred_result_2 = result_array[1]
    pred_result_3 = result_array[2]

    for result in pred_result_2:
        if result != predict_item_1:
                predict_item_2 = result
                break
            
    for result in pred_result_3:
        if result != predict_item_1:
                if result != predict_item_2:
                    predict_item_3 = result
                    break

    #Defining variables to deliver to html page (recommendations)
    predict_item_1_name = find_prod_info(predict_item_1)[1]
    predict_item_1_category = find_prod_info(predict_item_1)[0]
    predict_item_1_price = find_prod_info(predict_item_1)[2]
    predict_item_1_des = find_prod_info(predict_item_1)[3]
    predict_item_1_img = find_prod_info(predict_item_1)[4]
    predict_item_1_url = find_prod_info(predict_item_1)[5]

    predict_item_2_name = find_prod_info(predict_item_2)[1]
    predict_item_2_category = find_prod_info(predict_item_2)[0]
    predict_item_2_price = find_prod_info(predict_item_2)[2]
    predict_item_2_des = find_prod_info(predict_item_2)[3]
    predict_item_2_img = find_prod_info(predict_item_2)[4]
    predict_item_2_url = find_prod_info(predict_item_2)[5]

    predict_item_3_name = find_prod_info(predict_item_3)[1]
    predict_item_3_category = find_prod_info(predict_item_3)[0]
    predict_item_3_price = find_prod_info(predict_item_3)[2]
    predict_item_3_des = find_prod_info(predict_item_3)[3]
    predict_item_3_img = find_prod_info(predict_item_3)[4]
    predict_item_3_url = find_prod_info(predict_item_3)[5]

    return render_template("meandrecommend.html", Title='recommend',
                           name = name,
                           predict_item_1=predict_item_1,
                            predict_item_2=predict_item_2,
                            predict_item_3=predict_item_3,

                            predict_item_1_name=predict_item_1_name,
                            predict_item_1_category=predict_item_1_category,
                            predict_item_1_status=predict_item_1_category,
                            predict_item_1_price=predict_item_1_price,
                            predict_item_1_des=predict_item_1_des,
                            predict_item_1_img=predict_item_1_img,
                            predict_item_1_url=predict_item_1_url,

                            predict_item_2_name=predict_item_2_name,
                            predict_item_2_category=predict_item_2_category,
                            predict_item_2_status=predict_item_2_category,
                            predict_item_2_price=predict_item_2_price,
                            predict_item_2_des=predict_item_2_des,
                            predict_item_2_img=predict_item_2_img,
                            predict_item_2_url=predict_item_2_url,

                            predict_item_3_name=predict_item_3_name,
                            predict_item_3_category=predict_item_3_category,
                            predict_item_3_status=predict_item_3_category,
                            predict_item_3_price=predict_item_3_price,
                            predict_item_3_des=predict_item_3_des,
                            predict_item_3_img=predict_item_3_img,
                            predict_item_3_url=predict_item_3_url
                           )

if __name__ == '__main__':
    app.run(debug=True)
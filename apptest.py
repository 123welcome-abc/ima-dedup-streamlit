import os
import shutil
import pandas as pd
import streamlit as st
from PIL import Image
from pprint import pprint
from imagededup.methods import PHash
from imagededup.utils import plot_duplicates
from streamlit.components.v1 import html
import json
st.set_page_config(
    page_title="Imagededup Webapp",
    page_icon="🖼",
    layout="centered",
    initial_sidebar_state="auto",
)


#@st.cache(allow_output_mutation=True, show_spinner=False, suppress_st_warning=True)
@st.cache_data
#@st.cache_resource
def clean_directory(dir):
    for filename in os.listdir(dir):
        filepath = os.path.abspath(os.path.join(dir, filename))
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)

#@st.cache(allow_output_mutation=True, show_spinner=False, suppress_st_warning=True)
#@st.cache_resource
@st.cache_data
def create_dataframe():
    df = pd.DataFrame(columns=['duplicate_images'])
    return df

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

#@st.cache(allow_output_mutation=True, show_spinner=False, suppress_st_warning=True)
@st.cache_resource
##输入图片查重
def single_duplicate(uploaded_file,duplicates):
	name=uploaded_file
	dedup_shot = os.path.join('output/', 'dedup_shot.jpg')
	plot_duplicates(image_dir='output/', duplicate_map=duplicates, filename=name, outfile=dedup_shot)
#@st.cache(allow_output_mutation=True, show_spinner=False, suppress_st_warning=True)
#@st.cache_resource
@st.cache_data
def zidian(name):
	image_dir=name
	_hash = PHash()
	encodings={}
	file_path={}#文件路径字典
	for dirpath, dirnames, filenames in os.walk('.\\images'):
		
	    for dirname in dirnames:
		    encoding=_hash.encode_images(image_dir=os.path.join(dirpath, dirname))
		    encodings.update(encoding)
		    
	    for filename in filenames:
		    file_path[filename]=dirpath
		    
	#encodings = _hash.encode_images(image_dir=image_dir)
	dedup_json = os.path.join('output/', 'dedup.json')
	##dedup_json ='output/'
	deduplist_json=os.path.join('output/', 'deduplist.json')
	duplicates = _hash.find_duplicates(encoding_map=encodings, outfile=dedup_json)
	duplicates_list = _hash.find_duplicates_to_remove(encoding_map=encodings,outfile=deduplist_json) #保存需要移除的相似图像
	return duplicates,file_path
@st.cache(allow_output_mutation=True, show_spinner=False, suppress_st_warning=True)
def zidian2():
	image_dir='uploads/'
	_hash = PHash()
	encodings = _hash.encode_images(image_dir=image_dir)
	dedup_json = os.path.join('output/', 'dedup.json')
	##dedup_json ='output/'
	duplicates = _hash.find_duplicates(encoding_map=encodings, outfile=dedup_json)
	return duplicates

#@st.cache_data(allow_output_mutation=True, show_spinner=False, suppress_st_warning=False)
#@st.cache_resource 
#@st.cache_data
class upname:
    def __init__(self, name):
        self.name = name
if __name__ == '__main__':
    clean_directory("uploads/")

    main_image = Image.open('static/main_banner.png')
    st.image(main_image,use_column_width='auto')
    st.title("✨ Image Deduplicator 🏜")
    st.info(' Let me help you find exact and near duplicates in an image collection 😉')
    
    option2 = st.selectbox(
     'you can select some image',
     ('abra', 'alakazam'))
    
    #file_path={}
    file_folder = st.sidebar.text_input('输入数据集文件夹路径', value="") #.images//
    with st.spinner(f"Finding duplicates... This may take several minutes depending on the number of images uploaded 💫"):
	    if st.sidebar.button(label="生成字典"):
		    final_dup_imgs,file_path=zidian(file_folder)
		    with open(r"./output/filepath.json", "w") as f2:
			    js = json.dumps(file_path)
			    f2.write(js)
		

    ##上传数据集，需改进
    
    uploaded_files = st.file_uploader("上传文件 🚀", type=["png","jpg","bmp","jpeg"], accept_multiple_files=True)
    with st.spinner(f"Finding duplicates... This may take several minutes depending on the number of images uploaded 💫"):
        if uploaded_files:
            for uploaded_file in uploaded_files:
                with open(os.path.join("uploads/",uploaded_file.name),"wb") as f:
                    f.write((uploaded_file).getbuffer())
            final_dup_imgs=zidian2()
    
    ##chachong=st.button(label="生成字典",on_click=zidian) 
    #final_dup_imgs=zidian()

    ##上传需查重的图像
    uploaded_file = st.file_uploader("输入需查重的图片", type=["png","jpg","bmp","jpeg"])
    if uploaded_file is None:
	    #st.write(" ")
	    if option2 =="abra":
		    image=Image.open("image/abra.png")
		    uploaded_file=upname("abra.png")
	    else:
		    image=Image.open("image/alakazam.png")
		    uploaded_file=upname("alakazam.png")
	    st.image(image, caption=option2+".png", use_column_width=None)
    else:
	    image = Image.open(uploaded_file)
	    st.image(image, caption=uploaded_file.name, use_column_width=None)
	    ##st.write(uploaded_file)
    #chachong=st.button(label="查重",on_click=single_duplicate,args=(image,final_dup_imgs))
    #chachong=st.button(label="查重",on_click=None)
    
    if st.button(label="查重"):
	    #st.write(uploaded_file.name)
	    with open("./output/filepath.json", "r", encoding="utf-8") as imgf:
		    image_path = json.load(imgf)	    
		    with open("./output/dedup.json", "r", encoding="utf-8") as f:
			    content = json.load(f)
			    if(len(content[uploaded_file.name])>0):
					#group=[]
					#group.append(final_dup_imgs.items(uploaded_file.name))
					#st.write(final_dup_imgs.items(uploaded_file.name))#st.write("存在")
				    images=[]
				    caps=[]
				    for imgs in content[uploaded_file.name]:
					    img_dir=os.path.join(image_path[imgs],imgs)
					    img=Image.open(img_dir)
					    images.append(img)
					    caps.append(imgs)
				    st.success(f"相似或重复项如下:共{len(content[uploaded_file.name])}项")
				    st.image(images,caption=caps,use_column_width=None)
			    else:
				    st.warning("不存在相似或重复项")
	    
    if st.sidebar.button(label="分组"):
	    with st.spinner(f"正在分组,请稍后... 💫"):
		    groups = []
		    with open("./output/dedup.json", "r", encoding="utf-8") as f:
			    content = json.load(f)
			    for key, value in content.items():
				    if len(value)>0:
					    groups.append([key] + value)
		    #output_dir='E:\\my_image_dedup\\web\\myweb\\Streamlit-Imagededup-main\\similar'
		    output_dir='similar/'
			##print(len(groups))  
		    with open("./output/filepath.json", "r", encoding="utf-8") as imgf:
			    image_path = json.load(imgf)
			    for i, group in enumerate(groups):
				    sub_dir = os.path.join(output_dir, 'group_'+str(i)+'('+group[0]+')')
				    os.makedirs(sub_dir, exist_ok=True)
				    for image in group:
						#src = os.path.join(image_dir, image)
					    src = os.path.join(image_path[image], image)
					    dst = os.path.join(sub_dir, image)
					    shutil.copy(src, dst)
		    st.success("已分组完成，请勿重复操作")   
			
    if st.sidebar.button(label="输出重复项"):
		#duplicates_list = _hash.find_duplicates_to_remove(encoding_map=encodings,outfile=deduplist_json) #保存需要移除的相似图像
	    with open("./output/deduplist.json", "r", encoding="utf-8") as duplist:
		    duplicates_list = json.load(duplist)
		    with open("./output/filepath.json", "r", encoding="utf-8") as imgf:
			    image_path = json.load(imgf)
			    #similar_path='E:\\my_image_dedup\\web\\myweb\\Streamlit-Imagededup-main\\similar_images'
			    similar_path='similar_images/'
			    for filename in duplicates_list:
				    duplist_dir=os.path.join(similar_path,filename)#拼接成重复图像路径
				    src_dir=os.path.join(image_path[filename], filename)#原图
				    shutil.copy(src_dir, duplist_dir)
	    st.success("已完成，请勿重复操作")
    if st.sidebar.button(label="查看分组和重复项"):
	    st.write("test")
    if st.button(label="清空"):
	    clean_directory("uploads/")
	


    ##st.markdown("<br><hr><center>Made with ❤️ by <a href='mailto:ralhanprateek@gmail.com?subject=imagededup WebApp!&body=Please specify the issue you are facing with the app.'><strong>Prateek Ralhan</strong></a> with the help of [imagededup](https://github.com/idealo/imagededup) built by [idealo](https://github.com/idealo) ✨</center><hr>", unsafe_allow_html=True)
    ##st.markdown("<style> footer {visibility: hidden;} </style>", unsafe_allow_html=True)
    st.markdown('''<style>
/* button背景色 */ 
/*查重*/
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.egzxvld5 > div.block-container.css-1y4p8pa.egzxvld4 > div:nth-child(1) > div > div:nth-child(11) > div > button{
    background-color: #98F5FF;
    color: black;	
}
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.egzxvld5 > div.block-container.css-1y4p8pa.egzxvld4 > div:nth-child(1) > div > div:nth-child(12) > div > button{
    background-color: #98F5FF;
    color: black;	
}
/*分组*/
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.css-vk3wp9.e1fqkh3o11 > div.css-6qob1r.e1fqkh3o3 > div.css-e3xfei.e1fqkh3o4 > div > div:nth-child(1) > div > div:nth-child(3) > div > button{
    background-color: #98FB98;
    color: black;
}
/*输出重复项*/
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.css-vk3wp9.e1fqkh3o11 > div.css-6qob1r.e1fqkh3o3 > div.css-e3xfei.e1fqkh3o4 > div > div:nth-child(1) > div > div:nth-child(4) > div > button{
    background-color: #F08080;
    color: black;
}
/*查看重复项*/
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.css-vk3wp9.e1fqkh3o11 > div.css-6qob1r.e1fqkh3o3 > div.css-e3xfei.e1fqkh3o4 > div > div:nth-child(1) > div > div:nth-child(5) > div > button{
    background-color: #CAFF70;
    color: black;
}
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.css-vk3wp9.e1fqkh3o11 > div.css-6qob1r.e1fqkh3o3 > div.css-e3xfei.e1fqkh3o4 > div > div:nth-child(1) > div > div:nth-child(5) > div > button{
    background-color: #CAFF70;
    color: black;
}
/*清空*/
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.egzxvld5 > div.block-container.css-1y4p8pa.egzxvld4 > div:nth-child(1) > div > div:nth-child(13) > div > button{
    background-color: #98F5FF;
    color: black;	
}
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.egzxvld5 > div.block-container.css-1y4p8pa.egzxvld4 > div:nth-child(1) > div > div:nth-child(16) > div > button{
    background-color: #DDA0DD;
    color: black;
}
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.css-vk3wp9.e1fqkh3o11 > div.css-6qob1r.e1fqkh3o3 > div.css-e3xfei.e1fqkh3o4 > div > div:nth-child(1) > div > div:nth-child(2) > div > button{
    background-color: #98F5FF;
    color: black;
}
</style>''', unsafe_allow_html=True)	



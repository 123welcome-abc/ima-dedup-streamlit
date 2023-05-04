import os
import shutil
import pandas as pd
import streamlit as st
from PIL import Image
from pprint import pprint
from imagededup.methods import PHash
from imagededup.utils import plot_duplicates
import json
st.set_page_config(page_title="相似图像显示")
st.title("相似图像分组")
#st.markdown("# 测试子页面")
#similarpath='E:\\my_image_dedup\\web\\myweb\\Streamlit-Imagededup-main\\similar'
similarpath='similar/'
similars='./similar_images'
#file_list=next(os.walk(similarpath))
file_list=os.listdir(similarpath)
file_list.sort(key=lambda x: int(x.split("(")[0].split("_")[1]))  
#st.write(file_list)
similar_imgs_group=os.listdir(similars)
if len(file_list)>0:
    file_selected = st.sidebar.selectbox('选择文件', file_list)
    select_file=os.path.join(similarpath,file_selected)
    img_group=os.listdir(select_file)
    
    #cols=st.columns(len(img_group))
    st.info(f'已选择文件夹：{select_file}')
    st.success("当前分组:")
    imgs=[]
    caps=[]
    similars_imgs=[]
    similars_caps=[]
    for img in img_group:
	    image=Image.open(os.path.join(select_file,img))
	    imgs.append(image)
	    caps.append(img)
    st.image(imgs,caption=caps,use_column_width=None)
else:
	st.warning("您没有进行分组操作，请返回主页点击分组按钮...")

#st.write(similae_imgs_group)
st.write(" ")
st.write(" ")
st.write(" ")
if st.sidebar.button(label="数据集相似或重复项"):
    if len(similar_imgs_group)>0:
	    st.success(f"数据集中相似或重复图像如下:共{len(similar_imgs_group)}项")
	    for similars_img in similar_imgs_group:
		    image=Image.open(os.path.join(similars,similars_img))
		    similars_imgs.append(image)
		    similars_caps.append(similars_img)
	    st.image(similars_imgs,caption=similars_caps,use_column_width=None)
    else:
	    st.warning("您没有进行输出相似或重复图像的操作，或者该数据集下没有相似或重复图像...")
				
#st.write(select_file)
#st.write(img_group)
#st.image(select_file)
st.markdown('''<style>
/* button背景色 */ 
/*数据集相似或重复项*/
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.css-vk3wp9.e1fqkh3o11 > div.css-6qob1r.e1fqkh3o3 > div.css-e3xfei.e1fqkh3o4 > div > div:nth-child(1) > div > div:nth-child(2) > div > button{
    background-color: #98F5FF;
    color: black;	
}
</style>''', unsafe_allow_html=True)	

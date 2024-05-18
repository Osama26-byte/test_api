import gradio as gr
# from gfpgan import GFPGANer
# from basicsr.archs.rrdbnet_arch import RRDBNet
# from realesrgan import RealESRGANer
import numpy as np
import cv2
import requests

def gpt_api(passage, question, answer):
    print(passage)
    print(question)
    print(answer)

    return answer
    
interface = gr.Interface(
    fn=gpt_api,
    inputs=[gr.Textbox(label="Passage"), gr.Textbox(label="Question"), gr.Textbox(label="Answer")],
    outputs=gr.Textbox(label="Result"),
    title="MOOCHI",
    description="An advanced AI-driven educational tool revolutionizing the exam evaluation experience.",
    allow_flagging=False
)

submit_button = gr.Button("Submit")

interface.launch(server_name="192.168.1.101", server_port=8080, share=True)
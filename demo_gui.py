import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import torch
from diffusers import StableDiffusionPipeline

# ! Load model once (it is slow for anyone trying it so avoids repeated load wait for the pipelines to load to see the results)
# ! espialy if your devise gpu isn't supported

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU name:", torch.cuda.get_device_name(0))
else:
    print("❌ No GPU detected.")

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    revision="fp16" if torch.cuda.is_available() else None
).to(device)


"""
function to handles the full process of generating and displaying 
an image based on a text prompt entered by the user through the built in GUI.
"""


def generate_and_show(prompt):
    if not prompt.strip():
        messagebox.showerror("Error", "Please enter a valid prompt.")
        return

    image = pipe(prompt=prompt, guidance_scale=7.5).images[0]
    image.save("demo_outputs/demo_gui_result.png")

    img_window = tk.Toplevel(root)
    img_window.title("Generated Image")

    img = Image.open("demo_outputs/demo_gui_result.png")
    img = img.resize((512, 512))
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(img_window, image=photo)
    label.image = photo
    label.pack()


# * GUI setup
root = tk.Tk()
root.title("Text-to-Image Demo (Stable Diffusion)")
root.geometry("400x200")

tk.Label(root, text="Enter your prompt: ").pack(pady=10)
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

btn = tk.Button(root, text="Generate Image",
                command=lambda: generate_and_show(entry.get()))
btn.pack(pady=10)

root.mainloop()

import os
import time
import subprocess
import GPUtil
# pip install gputil


GPU_CODEC = {'NVIDIA': 'h264_nvenc', 'AMD': 'h264_amf',
             'Intel(R)': 'h264_qsv', 'Apple': 'h264_videotoolbox'}


def check_gpu() -> str:
    gpus = GPUtil.getGPUs()
    if not len(gpus):
        print('You don\'t have any GPUs')
        return ''
    return GPU_CODEC.get(gpus[0].name.split()[0], 'openh264')


def ffmpegEncode(folder_path: str, file_name: str, action: int) -> None:
    """
    using H.264 video codec to trasfer .ts file to .mp4 file
    action: 0 for not encoding, 1 for GPU encoding, 2 for CPU encoding
    """
    gpu_text = check_gpu()
    start_time = time.time()
    # 不轉檔: 0
    if action == 0:
        pass

    # GPU轉檔: 1
    elif action == 1 and gpu_text:
        os.chdir(folder_path)
        try:
            subprocess.run(['ffmpeg', '-i', f'{file_name}.ts', '-c:v', f'{gpu_text}', '-b:v', '10000K',
                            '-threads', '5', f'{file_name}.mp4'
                            ])
            print("GPU轉檔成功!")
            os.remove(f'{file_name}.ts')
        except Exception as e:
            print(f"GPU轉檔失敗! {e}")

    # CPU轉檔: 2
    else:
        os.chdir(folder_path)
        try:
            subprocess.run(['ffmpeg', '-i', f'{file_name}.ts', '-c:v', 'libx264', '-b:v', '3M',
                            '-threads', '5', '-preset', 'superfast', f'{file_name}.mp4'
                            ])
            print("CPU轉檔成功!")
            os.remove(f'{file_name}.ts')
        except Exception as e:
            print("CPU轉檔失敗! {e}")

    end_time = time.time()
    print(f'花費 {((end_time - start_time) / 60):.2f} 分鐘 合成完成 !')

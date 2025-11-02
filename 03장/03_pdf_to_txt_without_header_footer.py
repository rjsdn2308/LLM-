# 데이터 항목별 용량을 계산해주는 함수
def calc_storage(count, size_kb):
    """
    count : 파일 개수
    size_kb : 한 파일의 평균 크기(KB 단위)
    return : (bytes, MB, GB)
    """
    bytes_total = count * size_kb * 1024            # 총 바이트
    mb_total = bytes_total / (1024**2)              # MB
    gb_total = bytes_total / (1024**3)              # GB
    return bytes_total, mb_total, gb_total

# MVP 가정값
fruit_img_count, fruit_img_size = 1000, 200       # 장수, KB
fruit_video_count, fruit_video_size = 100, 30*1024  # 개수, MB→KB
text_count, text_size = 10000, 1                  # 레코드 수, KB
handwriting_count, handwriting_size = 20000, 100  # 장수, KB
gesture_count, gesture_size = 10000, 60           # 클립수, KB
model_size_mb = 500                               # 모델 MB

# 각 항목별 계산
fruit_img_bytes, fruit_img_mb, fruit_img_gb = calc_storage(fruit_img_count, fruit_img_size)
fruit_video_bytes, fruit_video_mb, fruit_video_gb = calc_storage(fruit_video_count, fruit_video_size)
text_bytes, text_mb, text_gb = calc_storage(text_count, text_size)
handwriting_bytes, handwriting_mb, handwriting_gb = calc_storage(handwriting_count, handwriting_size)
gesture_bytes, gesture_mb, gesture_gb = calc_storage(gesture_count, gesture_size)

# 모델(500MB) 바이트로 환산
model_bytes = model_size_mb * 1024 * 1024
model_mb = model_bytes / (1024**2)
model_gb = model_bytes / (1024**3)

# 합계
total_bytes = (fruit_img_bytes + fruit_video_bytes + text_bytes +
               handwriting_bytes + gesture_bytes + model_bytes)
total_mb = total_bytes / (1024**2)
total_gb = total_bytes / (1024**3)

# 백업/여유 20% 추가
backup_bytes = total_bytes * 1.2
backup_mb = backup_bytes / (1024**2)
backup_gb = backup_bytes / (1024**3)

# 결과 출력
print(f"과일 이미지: {fruit_img_mb:.2f} MB ({fruit_img_gb:.2f} GB)")
print(f"과일 비디오: {fruit_video_mb:.2f} MB ({fruit_video_gb:.2f} GB)")
print(f"텍스트 문제: {text_mb:.2f} MB ({text_gb:.4f} GB)")
print(f"손글씨 이미지: {handwriting_mb:.2f} MB ({handwriting_gb:.2f} GB)")
print(f"제스처(키포인트): {gesture_mb:.2f} MB ({gesture_gb:.2f} GB)")
print(f"모델: {model_mb:.2f} MB ({model_gb:.2f} GB)")
print("-"*50)
print(f"총합: {total_mb:.2f} MB ({total_gb:.2f} GB)")
print(f"백업(20%포함): {backup_mb:.2f} MB ({backup_gb:.2f} GB)")

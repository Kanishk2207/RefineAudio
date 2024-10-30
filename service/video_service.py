from moviepy.editor import VideoFileClip, AudioFileClip

class VideoProcessing:
    @staticmethod
    def merge_audio_with_video(video_path, processed_audio_path, output_video_path="./resources/final_output.mp4"):
        """Merges processed audio with the original video."""
        video = VideoFileClip(video_path)
        processed_audio = AudioFileClip(processed_audio_path)
        final_video = video.set_audio(processed_audio)
        final_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")

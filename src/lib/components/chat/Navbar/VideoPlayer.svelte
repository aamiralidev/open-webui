<script lang="ts">
  let muted = false;

  let videoDuration = "5:57";
  // Using a sample video from a public source
  let videoSrc =
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4";

  import { onMount, tick } from "svelte";

  let video;
  let playing = false;
  let progress = 0;
  let currentTime = "0:00";

  function togglePlay() {
    if (video.paused) {
      video.play();
      playing = true;
    } else {
      video.pause();
      playing = false;
    }
  }

  async function togglePiP() {
    if (document.pictureInPictureElement) {
      await document.exitPictureInPicture();
    } else {
      if (video !== document.pictureInPictureElement) {
        await video.requestPictureInPicture();
      }
    }
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      video.requestFullscreen();
    } else {
      document.exitFullscreen();
    }
  }

  function toggleMute() {
    video.muted = !video.muted;
    muted = video.muted;
  }

  function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes}:${secs < 10 ? "0" + secs : secs}`;
  }

  function updateProgress() {
    if (video) {
      progress = (video.currentTime / video.duration) * 100;
      currentTime = formatTime(video.currentTime);
    }
  }

  function seekVideo(e) {
    const rect = e.currentTarget.getBoundingClientRect();
    const pos = (e.clientX - rect.left) / rect.width;
    video.currentTime = pos * video.duration;
  }

  onMount(() => {
    if (video) {
      video.addEventListener("timeupdate", updateProgress);
    }

    return () => {
      if (video) {
        video.removeEventListener("timeupdate", updateProgress);
      }
    };
  });
</script>

<div class="video-container">
  <video
    bind:this={video}
    src={videoSrc}
    poster="/placeholder.svg?height=200&width=400"
    on:ended={() => (playing = false)}
    on:click={togglePlay}
  ></video>

  {#if !playing}
    <div class="video-overlay" on:click={togglePlay}>
      <button class="play-button">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="white"
          width="24"
          height="24"
        >
          <path d="M8 5v14l11-7z" />
        </svg>
      </button>
    </div>
  {/if}

  <div class="video-controls">
    <button class="play-small" on:click={togglePlay}>
      {#if playing}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="white"
          width="16"
          height="16"
        >
          <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
        </svg>
      {:else}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="white"
          width="16"
          height="16"
        >
          <path d="M8 5v14l11-7z" />
        </svg>
      {/if}
    </button>
    <span class="duration">{currentTime} / {videoDuration}</span>
    <div class="progress-bar" on:click={seekVideo}>
      <div class="progress-fill" style="width: {progress}%"></div>
    </div>
    <div class="right-controls">
      <button class="control-btn" on:click={togglePiP}>
        <svg
          xmlns="http://www.w3.org/2000/svg" 
          viewBox="0 0 24 24"
          fill="white"
          width="16"
          height="16"
        >
          <path
            d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 14H4V6h16v12z"
          />
        </svg>
      </button>
      <button class="control-btn" on:click={toggleMute}>
        {#if muted}
          <!-- Muted icon -->
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="white"
            viewBox="0 0 24 24"
            width="16"
            height="16"
          >
            <path
              d="M16.5 12L19 14.5 17.5 16 15 13.5 12.5 16 11 14.5 13.5 12 11 9.5 12.5 8 15 10.5 17.5 8 19 9.5 16.5 12zM4 9v6h4l5 5V4L8 9H4z"
            />
          </svg>
        {:else}
          <!-- Volume on icon -->
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="white"
            viewBox="0 0 24 24"
            width="16"
            height="16"
          >
            <path
              d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"
            />
          </svg>
        {/if}
      </button>
      <button class="control-btn" on:click={toggleFullscreen}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="white"
          width="16"
          height="16"
        >
          <path
            d="M19 19H5V5h7V3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2v-7h-2v7zM14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-7z"
          />
        </svg>
      </button>
    </div>
  </div>
</div>

<style>
  .video-container {
    position: relative;
    width: 100%;
    height: 200px;
    background-color: #111827;
    border-radius: 8px;
    overflow: hidden;
    margin-top: 10px;
  }

  video {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .video-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    background-color: rgba(0, 0, 0, 0.3);
  }

  .play-button {
    background-color: #6366f1;
    border: none;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }

  .video-controls {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 30px;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    padding: 0 10px;
  }

  .play-small {
    background: none;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    padding: 0;
    margin-right: 5px;
  }

  .duration {
    color: white;
    font-size: 12px;
    margin-right: 10px;
    white-space: nowrap;
  }

  .progress-bar {
    flex: 1;
    height: 4px;
    background-color: rgba(255, 255, 255, 0.3);
    border-radius: 2px;
    position: relative;
    cursor: pointer;
  }

  .progress-fill {
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    background-color: #6366f1;
    border-radius: 2px;
  }

  .right-controls {
    display: flex;
    margin-left: 10px;
  }

  .control-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    margin-left: 10px;
    display: flex;
    align-items: center;
  }
</style>

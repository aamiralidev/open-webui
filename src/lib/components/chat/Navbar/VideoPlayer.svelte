<script lang="ts">
  import { onMount, tick, createEventDispatcher } from 'svelte';

  export let src: string;
  export let durationLabel: string = '0:00';

  const dispatch = createEventDispatcher();

  let video;
  let playing = false;
  let progress = 0;
  let currentTime = '0:00';
  let showOverlay = false;

  function togglePlay() {
    if (video.paused) {
      video.play();
      playing = true;
    } else {
      video.pause();
      playing = false;
    }
  }

  function formatTime(seconds: number) {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes}:${secs < 10 ? '0' + secs : secs}`;
  }

  function updateProgress() {
    if (video) {
      progress = (video.currentTime / video.duration) * 100;
      currentTime = formatTime(video.currentTime);
    }
  }

  function seekVideo(e: MouseEvent) {
    const rect = (e.currentTarget as HTMLElement).getBoundingClientRect();
    const pos = (e.clientX - rect.left) / rect.width;
    video.currentTime = pos * video.duration;
  }

  async function showUpgradeOverlay() {
    showOverlay = true;
    await tick();
    window.createLemonSqueezy();
  }

  async function handlePurchase(url: string) {
    showOverlay = false;
    await tick();

    const tempBtn = document.createElement('a');
    tempBtn.href = url;
    tempBtn.className = 'lemonsqueezy-button';
    document.body.appendChild(tempBtn);
    window.createLemonSqueezy();
    tempBtn.click();
    document.body.removeChild(tempBtn);
  }

  function closeOverlay() {
    showOverlay = false;
  }

  onMount(() => {
    window.createLemonSqueezy?.();
    video?.addEventListener('timeupdate', updateProgress);

    return () => {
      video?.removeEventListener('timeupdate', updateProgress);
    };
  });
</script>

<div class="relative">
  <video bind:this={video} src={src} class="w-full rounded" on:click={togglePlay} />

  <div class="flex justify-between items-center mt-2 text-sm">
    <span>{currentTime}</span>
    <span>{durationLabel}</span>
  </div>

  <div class="w-full h-2 bg-gray-300 rounded cursor-pointer" on:click={seekVideo}>
    <div class="h-full bg-indigo-600 rounded" style="width: {progress}%;"></div>
  </div>

  <div class="flex mt-2 gap-2">
    <button class="bg-indigo-600 text-white px-4 py-1 rounded" on:click={togglePlay}>
      {playing ? 'Pause' : 'Play'}
    </button>
    <button class="bg-yellow-500 text-white px-4 py-1 rounded" on:click={showUpgradeOverlay}>
      Upgrade
    </button>
  </div>
</div>

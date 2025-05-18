<script>
  export let showPointer;
  export let showUpgradeOverlay;
  export let formatCredits;

  import VideoPlayer from "./VideoPlayer.svelte";
  import { user } from "$lib/stores";
  import { onMount, tick } from 'svelte';
  let tooltipEl;
  

  onMount(async () => {
    await tick(); // wait for DOM to render

    const tooltipRect = tooltipEl?.getBoundingClientRect();
    const viewportWidth = window.innerWidth;

    if (tooltipRect && tooltipRect.right > viewportWidth) {
      // Tooltip overflows to the right, shift it left
      const overflowAmount = tooltipRect.right - viewportWidth;
      tooltipEl.style.left = `calc(-50% - ${overflowAmount + 10}px)`; // Add 10px margin
    }

    if (tooltipRect && tooltipRect.left < 0) {
      // Tooltip overflows to the left, shift it right
      const overflowAmount = Math.abs(tooltipRect.left);
      tooltipEl.style.left = `calc(-50% + ${overflowAmount + 10}px)`;
    }
  });

  // Props for modal component
  const now = new Date();
  const creditResetsAt = $user.credit_resets_at
    ? new Date($user.credit_resets_at)
    : new Date(now.getFullYear(), 11, 31);

  const resetDays = Math.ceil((creditResetsAt - now) / (1000 * 60 * 60 * 24));

  const resetDate = creditResetsAt.toLocaleString("en-US", {
    month: "long",
    day: "numeric",
    hour: "numeric",
    minute: undefined,
    hour12: true,
    timeZoneName: "short",
    timeZone: "America/Los_Angeles", // for PST
  });
</script>

<div class="modal-wrapper" bind:this={tooltipEl}>
  {#if showPointer}
    <div class="pointer-triangle"></div>
  {/if}

  <div class="modal-container bg-white dark:bg-gray-900">
    <div class="progress-bar-overlay">
      <div
        class="progress-fill-overlay"
        style="width: {Math.ceil(
          (($user.credit_limit - $user.credits) / $user.credit_limit) * 100,
        )}%"
      ></div>
    </div>

    <h2 class="credits-header">
      {formatCredits($user.credit_limit - $user.credits)} / {formatCredits($user.credit_limit)} credits used this month
    </h2>
    <p class="reset-info">
      Credits reset in {resetDays} days ({resetDate})
    </p>

    <button class="add-credits-btn" on:click={showUpgradeOverlay}>
      Add more credits
    </button>

    <h3 class="how-it-works">How it Works:</h3>

    <p class="explanation">
      Credits get used every time you chat with the AI. The more videos, voice
      notes, docs, or websites you use to power up your chat... The more credits
      you invest.
    </p>

    <p class="explanation">
      You have {formatCredits($user.credit_limit)} credits per month. Once you
      run out of credits... You'll have to wait until next month or upgrade to a
      power user plan to unlock more credits and features!
    </p>

    <p class="footnote text-gray-500 dark:text-gray-500">
      * Unused credits don't roll over to the next month
    </p>
    <VideoPlayer />
  </div>
</div>

<style>

  .modal-wrapper {
    position: absolute;
    top: calc(100% + 10px);
    left: 50%;
    transform: translateX(-50%);
    z-index: 100000;
    width: 480px;
  }

  .pointer-triangle {
    width: 0;
    height: 0;
    border-left: 15px solid transparent;
    border-right: 15px solid transparent;
    border-bottom: 15px solid white;
    position: absolute;
    top: -15px;
    left: 50%;
    transform: translateX(-50%);
    filter: drop-shadow(0 -2px 2px rgba(0, 0, 0, 0.05));
    z-index: 10;
  }

  .modal-container {
    border-radius: 12px;
    padding: 20px;
    max-width: 480px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
      Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
    position: relative;
    z-index: 1000000;
  }

  .credits-header {
    font-size: 20px;
    font-weight: 600;
    margin: 0;
    margin-top: 10px;
    padding-left: 15px;
  }

  .reset-info {
    margin: 5px 0 20px 0;
    padding-left: 15px;
    color: #6366f1;
    font-size: 14px;
  }

  .add-credits-btn {
    background-color: #6366f1;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 14px;
    width: 100%;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    margin-bottom: 20px;
    transition: background-color 0.2s ease;
  }

  .add-credits-btn:hover {
    background-color: #4f46e5;
  }

  .how-it-works {
    font-size: 16px;
    font-weight: 600;
    margin: 0 0 10px 0;
  }

  .explanation {
    font-size: 14px;
    line-height: 1.5;
    margin-bottom: 15px;
  }

  .footnote {
    font-size: 12px;
    margin-bottom: 15px;
  }

  .progress-bar-overlay {
    height: 4px;
    background-color: #333;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 8px;
    position: relative;
  }

  .progress-fill-overlay {
    height: 100%;
    background: #7c3aed;
    border-radius: 4px;
    width: 1%;
  }

</style>

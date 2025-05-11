<svelte:head>
  <script src="https://app.lemonsqueezy.com/js/lemon.js" defer></script>
</svelte:head>

<script lang="ts">
	import { getContext } from 'svelte';
	import { toast } from 'svelte-sonner';

	import {
		WEBUI_NAME,
		banners,
		chatId,
		config,
		mobile,
		settings,
		showArchivedChats,
		showControls,
		showSidebar,
		temporaryChatEnabled,
		user
	} from '$lib/stores';

	import { slide } from 'svelte/transition';
	import { page } from '$app/stores';

	import ShareChatModal from '../chat/ShareChatModal.svelte';
	import ModelSelector from '../chat/ModelSelector.svelte';
	import Tooltip from '../common/Tooltip.svelte';
	import Menu from '$lib/components/layout/Navbar/Menu.svelte';
	import UserMenu from '$lib/components/layout/Sidebar/UserMenu.svelte';
	import MenuLines from '../icons/MenuLines.svelte';
	import AdjustmentsHorizontal from '../icons/AdjustmentsHorizontal.svelte';

	import PencilSquare from '../icons/PencilSquare.svelte';
	import Banner from '../common/Banner.svelte';

	// AI Credits Stuff Starts Here

	import { tweened } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';

	const animatedCredits = tweened(0, {
		duration: 400, // how fast (ms)
		easing: cubicOut
	});
	$: animatedCredits.set(Number($user.credits) || 0);
	$: if ($user && $user.credits !== undefined) {
    animatedCredits.set(Number($user.credits) || 0);
}
  let showPricingOverlay = false;
  let showCreditsTooltip = false;
	let buttonText = "Add more credits";
  let buttonColor = "#6366f1";

  // Props for modal component
  let creditsUsed = 25;
  let totalCredits = 2000;
  let resetDays = 28;
  let resetDate = "June 1 at 9am PST";
  let videoDuration = "5:57";

  // Using a sample video from a public source
  let videoSrc =
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4";

  import { onMount } from "svelte";

  let video;
  let playing = false;
  let progress = 0;
  let currentTime = "0:00";
  let showVideoControls = true;
  let showPointer = false;
  let showModal = false;
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

  function toggleModal() {
    showModal = !showModal;
    showPointer = showModal;
  }

  function showUpgradeOverlay() {
    showOverlay = true;
  }

  function closeOverlay() {
    showOverlay = false;
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

	const i18n = getContext('i18n');

	export let initNewChat: Function;
	export let title: string = $WEBUI_NAME;
	export let shareEnabled: boolean = false;

	export let chat;
	export let history;
	export let selectedModels;
	export let showModelSelector = true;

	let showShareChatModal = false;
	let showDownloadChatModal = false;
</script>

<ShareChatModal bind:show={showShareChatModal} chatId={$chatId} />

<nav class="sticky top-0 z-30 w-full py-1.5 -mb-8 flex flex-col items-center drag-region">
	<div class="flex items-center w-full px-1.5">
		<div
			class=" bg-linear-to-b via-50% from-white via-white to-transparent dark:from-gray-900 dark:via-gray-900 dark:to-transparent pointer-events-none absolute inset-0 -bottom-7 z-[-1]"
		></div>

		<div class=" flex max-w-full w-full mx-auto px-1 pt-0.5 bg-transparent">
			<div class="flex items-center w-full max-w-full">
				<div
					class="{$showSidebar
						? 'md:hidden'
						: ''} mr-1 self-start flex flex-none items-center text-gray-600 dark:text-gray-400"
				>
					<button
						id="sidebar-toggle-button"
						class="cursor-pointer px-2 py-2 flex rounded-xl hover:bg-gray-50 dark:hover:bg-gray-850 transition"
						on:click={() => {
							showSidebar.set(!$showSidebar);
						}}
						aria-label="Toggle Sidebar"
					>
						<div class=" m-auto self-center">
							<MenuLines />
						</div>
					</button>
				</div>

				<div
					class="flex-1 overflow-hidden max-w-full py-0.5
			{$showSidebar ? 'ml-1' : ''}
			"
				>
					{#if showModelSelector}
						<ModelSelector bind:selectedModels showSetDefault={!shareEnabled} />
					{/if}
				</div>

				<div class="self-start flex flex-none items-center text-gray-600 dark:text-gray-400">
					<!-- <div class="md:hidden flex self-center w-[1px] h-5 mx-2 bg-gray-300 dark:bg-stone-700" /> -->
					{#if shareEnabled && chat && (chat.id || $temporaryChatEnabled)}
						<Menu
							{chat}
							{shareEnabled}
							shareHandler={() => {
								showShareChatModal = !showShareChatModal;
							}}
							downloadHandler={() => {
								showDownloadChatModal = !showDownloadChatModal;
							}}
						>
							<button
								class="flex cursor-pointer px-2 py-2 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-850 transition"
								id="chat-context-menu-button"
							>
								<div class=" m-auto self-center">
									<svg
										xmlns="http://www.w3.org/2000/svg"
										fill="none"
										viewBox="0 0 24 24"
										stroke-width="1.5"
										stroke="currentColor"
										class="size-5"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											d="M6.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM12.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM18.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z"
										/>
									</svg>
								</div>
							</button>
						</Menu>
					{/if}
					<!-- Your AI Credits here -->
					<div class="relative w-fit mx-auto my-5"
							on:mouseenter={() => (showCreditsTooltip = true)}
							on:mouseleave={() => (showCreditsTooltip = false)}
							>
					  <div
							class="flex items-center gap-1 px-3 py-1 rounded-full bg-zinc-800 cursor-pointer text-lg font-semibold"
							on:click={() => (showPricingOverlay = true)}
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-5 w-5"
								fill="#FFD700"
								viewBox="0 0 24 24"
								stroke="#FFD700"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M13 10V3L4 14h7v7l9-11h-7z"
								/>
							</svg>
							{$animatedCredits.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 4 })}
						</div>
					
					  <!-- Tooltip Info -->
						{#if showCreditsTooltip}
							<div class="modal-wrapper">
        {#if showPointer}
          <div class="pointer-triangle"></div>
        {/if}

        <div class="modal-container">
          <div class="dot"></div>
          <h2 class="credits-header">
            {creditsUsed} / {totalCredits.toLocaleString()} credits used this month
          </h2>
          <p class="reset-info">
            Credits reset in {resetDays} days ({resetDate})
          </p>

          <button class="add-credits-btn" on:click={showUpgradeOverlay}>
            Add more credits
          </button>

          <h3 class="how-it-works">How it Works:</h3>

          <p class="explanation">
            Credits get used every time you chat with the AI. The more videos,
            voice notes, docs, or websites you use to power up your chat... The
            more credits you invest.
          </p>

          <p class="explanation">
            You have {totalCredits.toLocaleString()} credits per month. Once you
            run out of credits... You'll have to wait until next month or upgrade
            to a power user plan to unlock more credits and features!
          </p>

          <p class="footnote text-gray-500 dark:text-gray-500">
            * Unused credits don't roll over to the next month
          </p>

          <div class="video-container">
            <video
              bind:this={video}
              src={videoSrc}
              poster="/placeholder.svg?height=200&width=400"
              on:ended={() => (playing = false)}
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
                <button class="control-btn">
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
                <button class="control-btn">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="white"
                    width="16"
                    height="16"
                  >
                    <path
                      d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"
                    />
                  </svg>
                </button>
                <button class="control-btn">
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
        </div>
      </div>
						{/if}
						</div>

      {#if showOverlay}
    <div class="overlay">
      <div class="overlay-modal">
        <button class="close-button" on:click={closeOverlay}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="white"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>

        <div class="content">
          <h2 class="title">
            Wow, You're on Fire! <span class="fire-emoji">🔥</span>
          </h2>

          <div class="progress-container">
            <div class="progress-bar-overlay">
              <div class="progress-dot"></div>
              <div
                class="progress-fill-overlay"
                style="width: {(creditsUsed / totalCredits) * 100}%"
              ></div>
            </div>
            <div class="credits-text">
              {creditsUsed} / {totalCredits.toLocaleString()} credits used
            </div>
          </div>

          <p class="love-app">
            Looks like you really love the app, huh? <span class="emoji"
              >😊</span
            >
          </p>

          <h3 class="upgrade-title">
            Let's Get You Upgraded So You Can Go<br />
            Viral with Open WebUI <span class="fire-emoji">🔥</span>
          </h3>

          <div class="testimonial-section">
            <div class="avatars">
              <div class="avatar"></div>
              <div class="avatar"></div>
              <div class="avatar"></div>
              <div class="avatar"></div>
              <div class="avatar"></div>
            </div>

            <div class="rating-section">
              <div class="stars">
                <span class="star">★</span>
                <span class="star">★</span>
                <span class="star">★</span>
                <span class="star">★</span>
                <span class="star">★</span>
              </div>
              <div class="trusted-text">Trusted by 2000+ creators</div>
            </div>
          </div>

        <section class="">
        <div class="mx-auto flex flex-col sm:flex-row">
        <!-- Creator Plan -->
            <div 
              class="bg-gray-900 p-8 shadow ring-1 ring-gray-200"
              style="min-width: 450px"
            >
            <span class=" text-sm bg-white font-semibold text-gray-600 px-2 py-0.5 rounded">Most popular</span>
                <h3 class=" mt-3 text-xl font-semibold text-white">Creator</h3>
                <p class="mt-2 text-base text-white">Best for Small Creators. 2x monthly limit.</p>
                <p class="mt-8 text-4xl font-bold text-white">$40.33 <span
                        class="text-base font-normal text-white">per month</span></p>
                <p class="text-sm text-white">$484 billed annually</p>
                <a 
                href="https://creatorsystems.lemonsqueezy.com/buy/c865fef2-e816-4831-938b-3da1c7cb7322?embed=1" 
                class="mt-6 block text-center rounded-md border bg-indigo-600 text-white
                border-gray-800 px-4 py-3 text-lg font-medium text-indigo-600 hover:border-indigo-300"
                >
                    Start Free Trial
                </a>
                <ul class="mt-6 space-y-2 text-white text-sm text-gray-700">
                    <li class="text-base text-white">This includes:</li>
                    <li class="flex gap-1 items-center"><svg width="18px" height="18px" viewBox="0 0 24 24" fill="none"
                            xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" clip-rule="evenodd"
                                d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12ZM16.0303 8.96967C16.3232 9.26256 16.3232 9.73744 16.0303 10.0303L11.0303 15.0303C10.7374 15.3232 10.2626 15.3232 9.96967 15.0303L7.96967 13.0303C7.67678 12.7374 7.67678 12.2626 7.96967 11.9697C8.26256 11.6768 8.73744 11.6768 9.03033 11.9697L10.5 13.4393L12.7348 11.2045L14.9697 8.96967C15.2626 8.67678 15.7374 8.67678 16.0303 8.96967Z"
                                fill="#4f46e5" />
                        </svg> You get +2k EXTRA credits per month.</li>
                    <li class="flex gap-1 items-center"><svg width="18px" height="18px" viewBox="0 0 24 24" fill="none"
                            xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" clip-rule="evenodd"
                                d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12ZM16.0303 8.96967C16.3232 9.26256 16.3232 9.73744 16.0303 10.0303L11.0303 15.0303C10.7374 15.3232 10.2626 15.3232 9.96967 15.0303L7.96967 13.0303C7.67678 12.7374 7.67678 12.2626 7.96967 11.9697C8.26256 11.6768 8.73744 11.6768 9.03033 11.9697L10.5 13.4393L12.7348 11.2045L14.9697 8.96967C15.2626 8.67678 15.7374 8.67678 16.0303 8.96967Z"
                                fill="#4f46e5" />
                        </svg> 4k TOTAL monthly credits (2x monthly limit)</li>
                    <li class="flex gap-1 items-center"><svg width="18px" height="18px" viewBox="0 0 24 24" fill="none"
                            xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" clip-rule="evenodd"
                                d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12ZM16.0303 8.96967C16.3232 9.26256 16.3232 9.73744 16.0303 10.0303L11.0303 15.0303C10.7374 15.3232 10.2626 15.3232 9.96967 15.0303L7.96967 13.0303C7.67678 12.7374 7.67678 12.2626 7.96967 11.9697C8.26256 11.6768 8.73744 11.6768 9.03033 11.9697L10.5 13.4393L12.7348 11.2045L14.9697 8.96967C15.2626 8.67678 15.7374 8.67678 16.0303 8.96967Z"
                                fill="#4f46e5" />
                        </svg> Perfect for growing creators</li>
                </ul>
            </div>
            <!-- Creator Plus Plan -->
            <div
              class="bg-zinc-100 p-8 shadow-lg border border-gray-400"
              style="min-width: 450px"
            >
                <h3 class="text-xl font-semibold text-black">Creator+
                </h3>
                <p class="mt-2 text-base text-black text-gray-500">Best for Creators. 4x monthly limit (Save $12/mo).
                </p>
                <p class="mt-8 text-4xl font-bold text-black">$111 <span class="text-base font-normal text-black">per
                        month</span></p>
                <p class="text-sm text-black">$1,332 billed annually</p>
                <a href="https://creatorsystems.lemonsqueezy.com/buy/c865fef2-e816-4831-938b-3da1c7cb7322?embed=1" class="mt-6 block text-center rounded-md border bg-indigo-600 text-white
                border-indigo-200 px-4 py-3 text-lg font-medium text-indigo-600 hover:border-indigo-300">
                    Subscribe
                </a>
                <ul class="mt-6 space-y-2 text-sm text-black">
                    <li class="text-base ">This includes:</li>
                    <li class="flex gap-1 items-center"><svg width="18px" height="18px" viewBox="0 0 24 24" fill="none"
                            xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" clip-rule="evenodd"
                                d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12ZM16.0303 8.96967C16.3232 9.26256 16.3232 9.73744 16.0303 10.0303L11.0303 15.0303C10.7374 15.3232 10.2626 15.3232 9.96967 15.0303L7.96967 13.0303C7.67678 12.7374 7.67678 12.2626 7.96967 11.9697C8.26256 11.6768 8.73744 11.6768 9.03033 11.9697L10.5 13.4393L12.7348 11.2045L14.9697 8.96967C15.2626 8.67678 15.7374 8.67678 16.0303 8.96967Z"
                                fill="#898989" />
                        </svg> +6k EXTRA credits per month.</li>
                    <li class="flex gap-1 items-center"><svg width="18px" height="18px" viewBox="0 0 24 24" fill="none"
                            xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" clip-rule="evenodd"
                                d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12ZM16.0303 8.96967C16.3232 9.26256 16.3232 9.73744 16.0303 10.0303L11.0303 15.0303C10.7374 15.3232 10.2626 15.3232 9.96967 15.0303L7.96967 13.0303C7.67678 12.7374 7.67678 12.2626 7.96967 11.9697C8.26256 11.6768 8.73744 11.6768 9.03033 11.9697L10.5 13.4393L12.7348 11.2045L14.9697 8.96967C15.2626 8.67678 15.7374 8.67678 16.0303 8.96967Z"
                                fill="#898989" />
                        </svg> 8k TOTAL monthly credits (4x monthly limit)</li>
                    <li class="flex gap-1 items-center"><svg width="18px" height="18px" viewBox="0 0 24 24" fill="none"
                            xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" clip-rule="evenodd"
                                d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12ZM16.0303 8.96967C16.3232 9.26256 16.3232 9.73744 16.0303 10.0303L11.0303 15.0303C10.7374 15.3232 10.2626 15.3232 9.96967 15.0303L7.96967 13.0303C7.67678 12.7374 7.67678 12.2626 7.96967 11.9697C8.26256 11.6768 8.73744 11.6768 9.03033 11.9697L10.5 13.4393L12.7348 11.2045L14.9697 8.96967C15.2626 8.67678 15.7374 8.67678 16.0303 8.96967Z"
                                fill="#898989" />
                        </svg> Save $12/mo</li>
                    <li class="flex gap-1 items-center"><svg width="18px" height="18px" viewBox="0 0 24 24" fill="none"
                            xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" clip-rule="evenodd"
                                d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12ZM16.0303 8.96967C16.3232 9.26256 16.3232 9.73744 16.0303 10.0303L11.0303 15.0303C10.7374 15.3232 10.2626 15.3232 9.96967 15.0303L7.96967 13.0303C7.67678 12.7374 7.67678 12.2626 7.96967 11.9697C8.26256 11.6768 8.73744 11.6768 9.03033 11.9697L10.5 13.4393L12.7348 11.2045L14.9697 8.96967C15.2626 8.67678 15.7374 8.67678 16.0303 8.96967Z"
                                fill="#898989" />
                        </svg> Everything in Starter</li>
                </ul>
            </div>
            
        </div>
    </section>
        </div>
      </div>
    </div>
  {/if}

<!-- Your AI Credits end here -->

					<Tooltip content={$i18n.t('Controls')}>
						<button
							class=" flex cursor-pointer px-2 py-2 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-850 transition"
							on:click={async () => {
								await showControls.set(!$showControls);
							}}
							aria-label="Controls"
						>
							<div class=" m-auto self-center">
								<AdjustmentsHorizontal className=" size-5" strokeWidth="0.5" />
							</div>
						</button>
					</Tooltip>

					<Tooltip content={$i18n.t('New Chat')}>
						<button
							id="new-chat-button"
							class=" flex {$showSidebar
								? 'md:hidden'
								: ''} cursor-pointer px-2 py-2 rounded-xl text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-850 transition"
							on:click={() => {
								initNewChat();
							}}
							aria-label="New Chat"
						>
							<div class=" m-auto self-center">
								<PencilSquare className=" size-5" strokeWidth="2" />
							</div>
						</button>
					</Tooltip>

					{#if $user !== undefined && $user !== null}
						<UserMenu
							className="max-w-[200px]"
							role={$user?.role}
							on:show={(e) => {
								if (e.detail === 'archived-chat') {
									showArchivedChats.set(true);
								}
							}}
						>
							<button
								class="select-none flex rounded-xl p-1.5 w-full hover:bg-gray-50 dark:hover:bg-gray-850 transition"
								aria-label="User Menu"
							>
								<div class=" self-center">
									<img
										src={$user?.profile_image_url}
										class="size-6 object-cover rounded-full"
										alt="User profile"
										draggable="false"
									/>
								</div>
							</button>
						</UserMenu>
					{/if}
				</div>
			</div>
		</div>
	</div>

	{#if !history.currentId && !$chatId && ($banners.length > 0 || ($config?.license_metadata?.type ?? null) === 'trial' || (($config?.license_metadata?.seats ?? null) !== null && $config?.user_count > $config?.license_metadata?.seats))}
		<div class=" w-full z-30 mt-5">
			<div class=" flex flex-col gap-1 w-full">
				{#if ($config?.license_metadata?.type ?? null) === 'trial'}
					<Banner
						banner={{
							type: 'info',
							title: 'Trial License',
							content: $i18n.t(
								'You are currently using a trial license. Please contact support to upgrade your license.'
							)
						}}
					/>
				{/if}

				{#if ($config?.license_metadata?.seats ?? null) !== null && $config?.user_count > $config?.license_metadata?.seats}
					<Banner
						banner={{
							type: 'error',
							title: 'License Error',
							content: $i18n.t(
								'Exceeded the number of seats in your license. Please contact support to increase the number of seats.'
							)
						}}
					/>
				{/if}

				{#each $banners.filter( (b) => (b.dismissible ? !JSON.parse(localStorage.getItem('dismissedBannerIds') ?? '[]').includes(b.id) : true) ) as banner}
					<Banner
						{banner}
						on:dismiss={(e) => {
							const bannerId = e.detail;

							localStorage.setItem(
								'dismissedBannerIds',
								JSON.stringify(
									[
										bannerId,
										...JSON.parse(localStorage.getItem('dismissedBannerIds') ?? '[]')
									].filter((id) => $banners.find((b) => b.id === id))
								)
							);
						}}
					/>
				{/each}
			</div>
		</div>
	{/if}
</nav>


<style>

  .button-wrapper {
    position: relative;
    width: fit-content;
    margin: 20px auto;
  }

  .hover-button {
    background-color: var(--button-color);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 14px 28px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .modal-wrapper {
    position: absolute;
    top: calc(100% + 10px);
    left: -50%;
    transform: translateX(-50%);
    z-index: 1000;
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
    background-color: var(--color-gray-900, #0d0d0d);
    border-radius: 12px;
    padding: 20px;
    max-width: 480px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
      Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
    position: relative;
    z-index: 5;
  }

  .dot {
    width: 8px;
    height: 8px;
    background-color: #6366f1;
    border-radius: 50%;
    position: absolute;
    top: 20px;
    left: 20px;
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

  /* Overlay Modal Styles */
  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.75);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 100000;
  }

  .overlay-modal {
    background-color: #111;
    border-radius: 12px;
    width: 90%;
    max-width: 1040px;
    max-height: 90vh;
    overflow-y: auto;
    position: relative;
    color: white;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
  }

  .close-button {
    position: absolute;
    top: 16px;
    right: 16px;
    background: none;
    border: none;
    color: #999;
    cursor: pointer;
    z-index: 10;
    padding: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: color 0.2s;
  }

  .close-button:hover {
    color: white;
  }

  .content {
    padding: 40px 30px;
    padding-top: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .title {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 8px;
    color: white;
  }

  .fire-emoji {
    font-size: 1.1em;
  }

  .progress-container {
    width: 100%;
    max-width: 440px;
    margin-bottom: 24px;
  }

  .progress-bar-overlay {
    height: 4px;
    background-color: #333;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 8px;
    position: relative;
  }

  .progress-dot {
    width: 8px;
    height: 8px;
    background-color: #7c3aed;
    border-radius: 50%;
    position: absolute;
    top: -2px;
    left: 1%;
    z-index: 2;
  }

  .progress-fill-overlay {
    height: 100%;
    background: #7c3aed;
    border-radius: 4px;
    width: 1%;
  }

  .credits-text {
    font-size: 16px;
    color: white;
    text-align: left;
    margin-top: 4px;
  }

  .love-app {
    font-size: 20px;
    margin-bottom: 32px;
    display: flex;
    align-items: center;
    gap: 8px;
    color: white;
  }

  .emoji {
    font-size: 1.2em;
  }

  .upgrade-title {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 32px;
    line-height: 1.3;
    color: white;
  }

  .testimonial-section {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 30px;
    width: 100%;
    margin-bottom: 40px;
  }

  .avatars {
    display: flex;
  }

  .avatar {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background-color: #444;
    margin-left: -10px;
    border: 2px solid #111;
  }

  .avatar:first-child {
    margin-left: 0;
  }

  .rating-section {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .stars {
    display: flex;
    gap: 2px;
  }

  .star {
    color: #f59e0b;
    font-size: 20px;
  }

  .trusted-text {
    font-size: 14px;
    color: #e5e7eb;
  }

  .upgrade-button {
    background: #7c3aed;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 14px 28px;
    font-size: 18px;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
    max-width: 440px;
    transition: opacity 0.2s;
  }

  .upgrade-button:hover {
    opacity: 0.9;
  }

  /* Scrollbar styling */
  .overlay-modal::-webkit-scrollbar {
    width: 8px;
  }

  .overlay-modal::-webkit-scrollbar-track {
    background: #222;
    border-radius: 4px;
  }

  .overlay-modal::-webkit-scrollbar-thumb {
    background: #444;
    border-radius: 4px;
  }

  .overlay-modal::-webkit-scrollbar-thumb:hover {
    background: #555;
  }

  @media (min-width: 640px) {
    .content {
      padding: 48px 40px;
    }

    .title {
      font-size: 32px;
    }
  }
</style>

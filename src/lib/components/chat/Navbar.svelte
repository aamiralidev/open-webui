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
	import UpgradeOverlay from './Navbar/UpgradeOverlay.svelte';
	import CreditsExplanationTooltip from './Navbar/CreditsExplanationTooltip.svelte';

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

	let hideTimeout;

	function formatCredits(numStr) {
		const num = Number(numStr);
		const [int, dec] = num.toFixed(4).split('.');
		return int.replace(/\B(?=(\d{3})+(?!\d))/g, ',') + ',' + dec;
	}

	function showTooltip() {
		clearTimeout(hideTimeout);
		showCreditsTooltip = true;
	}

	function hideTooltip() {
		hideTimeout = setTimeout(() => {
			showCreditsTooltip = false;
		}, 150); // Adjust as needed
	}
	let showPricingOverlay = false;
	let showCreditsTooltip = false;

	// Props for modal component
	const creditResetsAt = new Date($user.credit_resets_at);
	const now = new Date();

	const resetDays = Math.ceil((creditResetsAt - now) / (1000 * 60 * 60 * 24));

	const resetDate = creditResetsAt.toLocaleString('en-US', {
		month: 'long',
		day: 'numeric',
		hour: 'numeric',
		minute: undefined,
		hour12: true,
		timeZoneName: 'short',
		timeZone: 'America/Los_Angeles' // for PST
	});

	let videoDuration = '5:57';
	// Using a sample video from a public source
	let videoSrc =
		'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4';

	import { onMount, tick } from 'svelte';

	let video;
	let playing = false;
	let progress = 0;
	let currentTime = '0:00';
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
		return `${minutes}:${secs < 10 ? '0' + secs : secs}`;
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

	async function showUpgradeOverlay() {
		showOverlay = true;
	}

	function closeOverlay() {
		showOverlay = false;
	}

	onMount(() => {
		window.createLemonSqueezy();
		if (video) {
			video.addEventListener('timeupdate', updateProgress);
		}

		return () => {
			if (video) {
				video.removeEventListener('timeupdate', updateProgress);
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
			<div
				class="flex items-center w-full max-w-full"
				style="flex-wrap: wrap; justify-content: end;"
			>
				<div
					class="{$showSidebar
						? 'md:hidden'
						: ''} mr-1 self-start flex items-center text-gray-600 dark:text-gray-400"
					style="flex-wrap: wrap;"
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
					class="flex-1 max-w-full py-0.5
			{$showSidebar ? 'ml-1' : ''}
			"
				>
					{#if showModelSelector}
						<ModelSelector bind:selectedModels showSetDefault={!shareEnabled} />
					{/if}
				</div>

				<div
					class="self-start flex items-center text-gray-600 dark:text-gray-400"
					style="flex-wrap: wrap;"
				>
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
					<div
						class="relative w-fit mx-auto my-5 mobile-responsive-btn"
						on:mouseenter={showTooltip}
						data-credits-trigger
					>
						<div
							class="flex items-center gap-1 px-3 py-1 rounded-full bg-gray-100 dark:bg-gray-800 cursor-pointer text-lg font-semibold"
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
							{formatCredits($animatedCredits)}
						</div>

						<!-- Tooltip Info -->
						{#if showCreditsTooltip}
							<CreditsExplanationTooltip bind:showPointer {showUpgradeOverlay} {formatCredits} />
						{/if}
					</div>

					<button
						class="upgrade-button-nav mx-3 px-4 py-1 border border-gray-300 dark:border-gray-600 rounded-full bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-100 font-semibold hover:bg-gray-50 dark:hover:bg-gray-800 transition"
						on:click={() => (showOverlay = true)}
					>
						Upgrade
					</button>

					{#if showOverlay}
						<UpgradeOverlay {closeOverlay} />
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
	@media (max-width: 420px) {
		.upgrade-button-nav {
			display: none;
		}
	}
</style>

<script>
	export let closeOverlay;
	export let onboarding = false;
	function formatCredits(numStr) {
		const num = Number(numStr);
		const [int, dec] = num.toFixed(4).split('.');
		return int.replace(/\B(?=(\d{3})+(?!\d))/g, ',') + ',' + dec;
	}

	import { user } from '$lib/stores';
	import { onMount, tick } from 'svelte';

	onMount(() => {
		window.createLemonSqueezy();
	});

	async function handleStartFreeTrial() {
		closeOverlay();
		await tick(); // Wait for DOM update

		// Step 2: Create a temporary button and trigger the click
		const tempBtn = document.createElement('a');
		tempBtn.href =
			'https://creatorsystems.lemonsqueezy.com/buy/c865fef2-e816-4831-938b-3da1c7cb7322?embed=1';
		tempBtn.className = 'lemonsqueezy-button';
		document.body.appendChild(tempBtn);
		window.createLemonSqueezy();
		tempBtn.click(); // This will trigger LemonSqueezy's overlay
		document.body.removeChild(tempBtn); // Clean up
	}

	async function handleBuyCreatorPlus() {
		closeOverlay();
		await tick(); // Wait for DOM update

		// Step 2: Create a temporary button and trigger the click
		const tempBtn = document.createElement('a');
		tempBtn.href =
			'https://creatorsystems.lemonsqueezy.com/buy/c865fef2-e816-4831-938b-3da1c7cb7322?embed=1';
		tempBtn.className = 'lemonsqueezy-button';
		document.body.appendChild(tempBtn);
		window.createLemonSqueezy();
		tempBtn.click(); // This will trigger LemonSqueezy's overlay
		document.body.removeChild(tempBtn); // Clean up
	}
</script>

<svelte:head>
	<script src="https://app.lemonsqueezy.com/js/lemon.js" defer></script>
</svelte:head>

<div class="overlay">
	<div class="overlay-modal bg-white dark:bg-gray-900 scrollbar-theme">
		{#if !onboarding}
			<button class="close-button" on:click={closeOverlay}>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="w-6 h-6 stroke-black dark:stroke-white"
					width="24"
					height="24"
					viewBox="0 0 24 24"
					fill="none"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				>
					<line x1="18" y1="6" x2="6" y2="18"></line>
					<line x1="6" y1="6" x2="18" y2="18"></line>
				</svg>
			</button>
		{/if}

		<div class="content">
			<h1 class="title text-black dark:text-white">
				Wow, You're on Fire! <span class="fire-emoji">🔥</span>
			</h1>

			<div class="progress-container">
				<div class="progress-bar-overlay">
					<div
						class="progress-fill-overlay"
						style="width: {Math.ceil(
							(($user.credit_limit - $user.credits) / $user.credit_limit) * 100
						)}%"
					></div>
				</div>
				<div class="credits-text">
					{formatCredits($user.credit_limit - $user.credits)} / {formatCredits($user.credit_limit)} credits
					used
				</div>
			</div>

			<p class="love-app">
				Looks like you really love the app, huh? <span class="emoji">😊</span>
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
				<div
					class="mx-auto flex flex-col sm:flex sm:flex-row sm:flex-wrap sm:justify-center sm:gap-[14px]"
				>
					<!-- Creator Plan -->
					<div class="bg-gray-900 p-8 shadow ring-1 ring-gray-200">
						<span class=" text-sm bg-white font-semibold text-gray-600 px-2 py-0.5 rounded"
							>Most popular</span
						>
						<h3 class=" mt-3 text-xl font-semibold text-white">Creator</h3>
						<p class="mt-2 text-base text-white">Best for Small Creators. 2x monthly limit.</p>
						<p class="mt-8 text-4xl font-bold text-white">
							$49 <span class="text-base font-normal text-white">per month</span>
						</p>
						<button
							on:click={handleStartFreeTrial}
							class="mt-6 block text-center rounded-md border bg-indigo-600 text-white w-full
                border-gray-800 px-4 py-3 text-lg font-medium text-indigo-600 hover:border-indigo-300"
						>
							Start Free Trial
						</button>
						<ul class="mt-6 space-y-2 text-white text-sm text-gray-700">
							<li class="text-base text-white">This includes:</li>
							<!-- 
							
							<li class="flex gap-1 items-center">
								 
							</li> -->
              <li class="flex gap-1" style="align-items: flex-start;">
								<div>
									<svg
									width="18px"
									height="18px"
									viewBox="0 0 24 24"
									fill="none"
									xmlns="http://www.w3.org/2000/svg"
								>
									<path
										fill-rule="evenodd"
										clip-rule="evenodd"
										d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12ZM16.0303 8.96967C16.3232 9.26256 16.3232 9.73744 16.0303 10.0303L11.0303 15.0303C10.7374 15.3232 10.2626 15.3232 9.96967 15.0303L7.96967 13.0303C7.67678 12.7374 7.67678 12.2626 7.96967 11.9697C8.26256 11.6768 8.73744 11.6768 9.03033 11.9697L10.5 13.4393L12.7348 11.2045L14.9697 8.96967C15.2626 8.67678 15.7374 8.67678 16.0303 8.96967Z"
										fill="#4f46e5"
									/>
								</svg> 
								</div>
								<div style="text-align: left;">
									<p>You get +2k EXTRA credits per month.</p>
								</div>
							</li>
							<li class="flex gap-1" style="align-items: flex-start;">
								<div>
                  <svg
									width="18px"
									height="18px"
									viewBox="0 0 24 24"
									fill="none"
									xmlns="http://www.w3.org/2000/svg"
								>
									<path
										fill-rule="evenodd"
										clip-rule="evenodd"
										d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12ZM16.0303 8.96967C16.3232 9.26256 16.3232 9.73744 16.0303 10.0303L11.0303 15.0303C10.7374 15.3232 10.2626 15.3232 9.96967 15.0303L7.96967 13.0303C7.67678 12.7374 7.67678 12.2626 7.96967 11.9697C8.26256 11.6768 8.73744 11.6768 9.03033 11.9697L10.5 13.4393L12.7348 11.2045L14.9697 8.96967C15.2626 8.67678 15.7374 8.67678 16.0303 8.96967Z"
										fill="#4f46e5"
									/>
								</svg>
								</div>
								<div style="text-align: left;">
									<p>4k TOTAL monthly credits (2x monthly limit)</p>
								</div>
							</li>
							<li class="flex gap-1" style="align-items: flex-start;">
								<div>
									<svg
									width="18px"
									height="18px"
									viewBox="0 0 24 24"
									fill="none"
									xmlns="http://www.w3.org/2000/svg"
								>
									<path
										fill-rule="evenodd"
										clip-rule="evenodd"
										d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12ZM16.0303 8.96967C16.3232 9.26256 16.3232 9.73744 16.0303 10.0303L11.0303 15.0303C10.7374 15.3232 10.2626 15.3232 9.96967 15.0303L7.96967 13.0303C7.67678 12.7374 7.67678 12.2626 7.96967 11.9697C8.26256 11.6768 8.73744 11.6768 9.03033 11.9697L10.5 13.4393L12.7348 11.2045L14.9697 8.96967C15.2626 8.67678 15.7374 8.67678 16.0303 8.96967Z"
										fill="#4f46e5"
									/>
								</svg>
								</div>
								<div style="text-align: left;">
									<p>Perfect for growing creators</p>
								</div>
							</li>
						
						</ul>
					</div>
					<!-- Creator Plus Plan -->
					<div class="bg-zinc-100 p-8 shadow-lg border border-gray-900">
						<h3 class="text-xl font-semibold text-black">Creator+</h3>
						<p class="mt-2 text-center text-black text-gray-500">
							Best for Creators. 4x monthly limit.
						</p>
						<p class="mt-8 text-4xl font-bold text-black">
							$99 <span class="text-base font-normal text-black">per month</span>
						</p>
						<button
							class="mt-6 block text-center rounded-md border bg-indigo-600 text-white w-full
                border-indigo-200 px-4 py-3 text-lg font-medium text-indigo-600 hover:border-indigo-300"
							on:click={handleBuyCreatorPlus}
						>
							Subscribe
						</button>
						<ul class="mt-6 space-y-2 text-sm text-black">
							<li class="text-base">This includes:</li>
							<li class="flex gap-1" style="align-items: flex-start;">
								<div>
									<svg
										width="18px"
										height="18px"
										viewBox="0 0 24 24"
										fill="none"
										xmlns="http://www.w3.org/2000/svg"
									>
										<path
											fill-rule="evenodd"
											clip-rule="evenodd"
											d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12ZM16.0303 8.96967C16.3232 9.26256 16.3232 9.73744 16.0303 10.0303L11.0303 15.0303C10.7374 15.3232 10.2626 15.3232 9.96967 15.0303L7.96967 13.0303C7.67678 12.7374 7.67678 12.2626 7.96967 11.9697C8.26256 11.6768 8.73744 11.6768 9.03033 11.9697L10.5 13.4393L12.7348 11.2045L14.9697 8.96967C15.2626 8.67678 15.7374 8.67678 16.0303 8.96967Z"
											fill="#898989"
										/>
									</svg>
								</div>
								<div style="text-align: left;">
									<p>+6k EXTRA credits per month.</p>
								</div>
							</li>
							<li class="flex gap-1" style="align-items: flex-start;">
								<div>
									<svg
										width="18px"
										height="18px"
										viewBox="0 0 24 24"
										fill="none"
										xmlns="http://www.w3.org/2000/svg"
									>
										<path
											fill-rule="evenodd"
											clip-rule="evenodd"
											d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12ZM16.0303 8.96967C16.3232 9.26256 16.3232 9.73744 16.0303 10.0303L11.0303 15.0303C10.7374 15.3232 10.2626 15.3232 9.96967 15.0303L7.96967 13.0303C7.67678 12.7374 7.67678 12.2626 7.96967 11.9697C8.26256 11.6768 8.73744 11.6768 9.03033 11.9697L10.5 13.4393L12.7348 11.2045L14.9697 8.96967C15.2626 8.67678 15.7374 8.67678 16.0303 8.96967Z"
											fill="#898989"
										/>
									</svg>
								</div>
								<div style="text-align: left;">
									<p>8k TOTAL monthly credits (4x monthly limit)</p>
								</div>
							</li>
							<li class="flex gap-1" style="align-items: flex-start;">
								<div>
									<svg
										width="18px"
										height="18px"
										viewBox="0 0 24 24"
										fill="none"
										xmlns="http://www.w3.org/2000/svg"
									>
										<path
											fill-rule="evenodd"
											clip-rule="evenodd"
											d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12ZM16.0303 8.96967C16.3232 9.26256 16.3232 9.73744 16.0303 10.0303L11.0303 15.0303C10.7374 15.3232 10.2626 15.3232 9.96967 15.0303L7.96967 13.0303C7.67678 12.7374 7.67678 12.2626 7.96967 11.9697C8.26256 11.6768 8.73744 11.6768 9.03033 11.9697L10.5 13.4393L12.7348 11.2045L14.9697 8.96967C15.2626 8.67678 15.7374 8.67678 16.0303 8.96967Z"
											fill="#898989"
										/>
									</svg>
								</div>
								<div style="text-align: left;">
									<p>Save $12/mo</p>
								</div>
							</li>
							<li class="flex gap-1" style="align-items: flex-start;">
								<div>
									<svg
										width="18px"
										height="18px"
										viewBox="0 0 24 24"
										fill="none"
										xmlns="http://www.w3.org/2000/svg"
									>
										<path
											fill-rule="evenodd"
											clip-rule="evenodd"
											d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12ZM16.0303 8.96967C16.3232 9.26256 16.3232 9.73744 16.0303 10.0303L11.0303 15.0303C10.7374 15.3232 10.2626 15.3232 9.96967 15.0303L7.96967 13.0303C7.67678 12.7374 7.67678 12.2626 7.96967 11.9697C8.26256 11.6768 8.73744 11.6768 9.03033 11.9697L10.5 13.4393L12.7348 11.2045L14.9697 8.96967C15.2626 8.67678 15.7374 8.67678 16.0303 8.96967Z"
											fill="#898989"
										/>
									</svg>
								</div>
								<div style="text-align: left;">
									<p>Everything in Starter</p>
								</div>
							</li>
						</ul>
					</div>
				</div>
			</section>
		</div>
	</div>
</div>

<style>
	.overlay {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 100000;
	}

	.overlay-modal {
		border-radius: 12px;
		width: 90%;
		max-width: 1040px;
		max-height: 90vh;
		overflow-y: auto;
		position: relative;
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
		text-align: left;
		margin-top: 4px;
	}

	.love-app {
		font-size: 20px;
		margin-bottom: 32px;
		display: flex;
		align-items: center;
		gap: 8px;
	}

	.emoji {
		font-size: 1.2em;
	}

	.upgrade-title {
		font-size: 22px;
		font-weight: 700;
		margin-bottom: 32px;
		line-height: 1.3;
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
		border-radius: 4px;
	}

	.overlay-modal::-webkit-scrollbar-thumb {
		border-radius: 4px;
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

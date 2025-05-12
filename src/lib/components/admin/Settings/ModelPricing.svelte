<script lang="ts">
  import { onMount } from 'svelte';
  import { getModelPricing, updateModelPricing } from '$lib/apis/modelPricing';
  import { toast } from 'svelte-sonner';

  const dummyModelPricing = [
    {
      model_id: "dummyModel",
      max_output_tokens: 4096,
      input_price_per_million_token: 60.0,
      output_price_per_million_token: 120.0
    }
  ];

  let modelPricingJSON = '';
  let originalValue = '';
  let isValid = true;
  let validationError = '';

  const getToken = () => localStorage.token;

  const validateJSON = (value: string) => {
    try {
      const parsed = JSON.parse(value);

      if (!Array.isArray(parsed)) {
        throw new Error('JSON must be an array.');
      }

      const ids = new Set();
      for (const entry of parsed) {
        if (!entry.model_id) throw new Error('Each entry must have a model_id.');
        if (ids.has(entry.model_id)) throw new Error(`Duplicate model_id: ${entry.model_id}`);
        ids.add(entry.model_id);
      }

      validationError = '';
      isValid = true;
    } catch (err: any) {
      validationError = err.message || 'Invalid JSON';
      isValid = false;
    }
  };

  const savePricing = async () => {
    if (!isValid || modelPricingJSON === originalValue) {
      toast.info('No changes to save.');
      return;
    }

    try {
      const pricing = JSON.parse(modelPricingJSON);
      const token = getToken();
      await updateModelPricing(pricing, token);
      toast.success('Model pricing updated successfully.');
      originalValue = modelPricingJSON;
    } catch (err) {
      console.error(err);
      toast.error(err?.detail || 'Failed to update model pricing.');
    }
  };

  const cancelChanges = () => {
    modelPricingJSON = originalValue;
    validateJSON(modelPricingJSON);
  };

  onMount(async () => {
    try {
      const token = getToken();
      const data = await getModelPricing(token);
      modelPricingJSON = JSON.stringify(data.length ? data : dummyModelPricing, null, 2);
      originalValue = modelPricingJSON;
      validateJSON(modelPricingJSON);
    } catch (err) {
      console.error('Failed to fetch model pricing:', err);
      modelPricingJSON = JSON.stringify(dummyModelPricing, null, 2);
      originalValue = modelPricingJSON;
      validationError = 'Could not load model pricing, showing defaults.';
      isValid = false;
    }
  });
</script>


<div class="space-y-2">
  <h2 class="text-sm font-semibold text-gray-700 dark:text-gray-200">Model Pricing</h2>

  <textarea
    bind:value={modelPricingJSON}
    on:input={(e) => validateJSON(e.target.value)}
    rows="20"
    class="w-[99%] p-2 text-sm font-mono rounded border border-gray-300 dark:border-gray-700 dark:bg-gray-850 dark:text-gray-100 
      focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-0 ml-1"
  ></textarea>

  {#if !isValid}
    <div class="text-red-500 text-xs">{validationError}</div>
  {/if}

  <div class="flex justify-end gap-2">
    <button
      class="px-4 py-2 text-sm rounded bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-50"
      on:click={savePricing}
      disabled={!isValid}
    >
      Save
    </button>
  </div>
</div>

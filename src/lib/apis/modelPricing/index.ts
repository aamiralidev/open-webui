import { WEBUI_API_BASE_URL } from '$lib/constants';
import type { ModelPricingModel } from '$lib/types';

export const getModelPricing = async (token: string = ''): Promise<ModelPricingModel[]> => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/model-pricing/`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      authorization: `Bearer ${token}`
    }
  })
    .then(async (res) => {
      if (!res.ok) throw await res.json();
      return res.json();
    })
    .catch((err) => {
      error = err;
      console.error('getModelPricing error:', err);
      return null;
    });

  if (error) {
    throw error;
  }

  return res;
};

export const updateModelPricing = async (
  pricing: ModelPricingModel[],
  token: string = ''
): Promise<boolean> => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/model-pricing/update`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      authorization: `Bearer ${token}`
    },
    body: JSON.stringify(pricing)
  })
    .then(async (res) => {
      if (!res.ok) throw await res.json();
      return true;
    })
    .catch((err) => {
      error = err;
      console.error('updateModelPricing error:', err);
      return false;
    });

  if (error) {
    throw error;
  }

  return res;
};

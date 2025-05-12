export type Banner = {
	id: string;
	type: string;
	title?: string;
	content: string;
	url?: string;
	dismissible?: boolean;
	timestamp: number;
};

export enum TTS_RESPONSE_SPLIT {
	PUNCTUATION = 'punctuation',
	PARAGRAPHS = 'paragraphs',
	NONE = 'none'
}

export interface ModelPricingModel {
	model_id: string;
	max_output_tokens: number;
	input_price_per_million_token: string;
	output_price_per_million_token: string;
}


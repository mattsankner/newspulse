export interface Article {
  id: string;
  title: string;
  description?: string;
  content?: string;
  url: string;
  source_id?: string;
  source_name: string;
  author?: string;
  published_at: string;
  url_to_image?: string;
}

export enum PoliticalStance {
  LEFT = 'left',
  CENTER = 'center',
  RIGHT = 'right',
  UNKNOWN = 'unknown'
}

export interface Classification {
  article_id: string;
  stance: PoliticalStance;
  confidence: number;
}

export interface Consensus {
  id: string;
  topic: string;
  summary: string;
  left_points: string[];
  center_points: string[];
  right_points: string[];
  common_ground: string[];
} 
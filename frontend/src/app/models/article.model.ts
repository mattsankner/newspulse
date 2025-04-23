export interface Article {
  id: string;
  title: string;
  description: string;
  content?: string;
  url: string;
  source_id?: string;
  source_name: string;
  author?: string;
  published_at: string;
  url_to_image?: string;
  political_stance?: string;
  classification?: Classification;
  raw_data?: any;
}

export enum PoliticalStance {
  Left = 'left',
  Center = 'center',
  Right = 'right'
}

export interface Classification {
  id: number;
  topic: string;
  summary: string;
  left_points: string[];
  center_points: string[];
  right_points: string[];
  common_ground: string[];
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
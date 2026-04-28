// There are two possible execution paths:
//
// - Web path:
//   Browse external sources, summarize the retrieved content,
//   and include source URLs in the response.
//
// - Direct path:
//   Answer using the model's existing knowledge without web access.
//
// Both paths produce the same response shape.

export type candidate = {
  answer: string;

  // List of source URLs used to generate the answer.
  // Empty when the response is generated directly from the model.
  sources: string[];

  // Indicates whether the answer was generated from web content
  // or directly from the model's knowledge.
  mode: 'web' | 'direct';
};

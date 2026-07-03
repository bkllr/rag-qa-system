/**
 * SSE 流式聊天 API 封装
 * 基于 fetch + ReadableStream 实现，支持 AbortController 取消请求。
 */

/**
 * 发起流式 RAG 聊天请求。
 *
 * @param {string} question - 用户问题
 * @param {Object} callbacks - 回调函数
 * @param {Function} callbacks.onToken - 接收到新 token 时调用
 * @param {Function} callbacks.onSource - 接收到来源引用时调用
 * @param {Function} callbacks.onDone - 流结束时调用
 * @param {Function} callbacks.onError - 出错时调用
 * @returns {Function} cancel - 取消请求的函数
 */
export function streamChat(question, { onToken, onSource, onDone, onError }) {
  const controller = new AbortController();

  fetch("/api/chat/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
    signal: controller.signal,
  })
    .then(async (response) => {
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        // SSE 数据以 \n\n 分隔
        const parts = buffer.split("\n\n");
        buffer = parts.pop(); // 保留不完整的最后一个片段

        for (const part of parts) {
          if (!part.startsWith("data: ")) continue;

          try {
            const data = JSON.parse(part.slice(6));

            switch (data.type) {
              case "token":
                onToken(data.content);
                break;
              case "sources":
                onSource(data.sources);
                break;
              case "done":
                onDone();
                break;
              case "error":
                onError(new Error(data.content));
                break;
            }
          } catch (e) {
            // 忽略解析失败的数据块
          }
        }
      }
    })
    .catch((err) => {
      if (err.name === "AbortError") return;
      onError(err);
    });

  // 返回取消函数
  return () => controller.abort();
}

import { useCallback, useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  Bot,
  Plus,
  Send,
  Trash2,
  MessageSquare,
  Sparkles,
  BookOpen,
  LoaderCircle,
  AlertCircle,
  GraduationCap,
  Code2,
  Lightbulb,
} from "lucide-react";

import DashboardLayout from "../components/DashboardLayout";
import api from "../services/api";
import "./AITutor.css";

const SUGGESTED_PROMPTS = [
  {
    icon: BookOpen,
    title: "Explain a concept",
    prompt: "Explain supervised learning with a simple example.",
  },
  {
    icon: Code2,
    title: "Help me with code",
    prompt: "Explain the difference between a stack and a queue with code examples.",
  },
  {
    icon: Lightbulb,
    title: "Prepare for exams",
    prompt: "Give me important points to prepare for my next computer science exam.",
  },
];

function AITutor() {
  const [courses, setCourses] = useState([]);
  const [topics, setTopics] = useState([]);

  const [selectedCourse, setSelectedCourse] = useState("");
  const [selectedTopic, setSelectedTopic] = useState("");

  const [conversations, setConversations] = useState([]);
  const [activeConversationId, setActiveConversationId] = useState(null);
  const [messages, setMessages] = useState([]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(true);
  const [loadingTopics, setLoadingTopics] = useState(false);
  const [loadingConversation, setLoadingConversation] = useState(false);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");

  const isExistingConversation = activeConversationId !== null;

  const fetchHistory = useCallback(async () => {
    try {
      const response = await api.get("/ai-tutor/history", {
        params: { limit: 100, offset: 0 },
      });

      setConversations(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to load your conversation history."
      );
    }
  }, []);

  useEffect(() => {
    let mounted = true;

    const initialize = async () => {
      try {
        const [courseResponse, historyResponse] = await Promise.all([
          api.get("/courses/"),
          api.get("/ai-tutor/history", {
            params: { limit: 100, offset: 0 },
          }),
        ]);

        if (!mounted) return;

        setCourses(courseResponse.data);
        setConversations(historyResponse.data);
        setError("");
      } catch (err) {
        if (!mounted) return;

        setError(
          err.response?.data?.detail ||
            "Unable to initialize AI Tutor. Please try again."
        );
      } finally {
        if (mounted) setLoading(false);
      }
    };

    initialize();

    return () => {
      mounted = false;
    };
  }, []);

  const fetchTopics = async (courseId) => {
    if (!courseId) {
      setTopics([]);
      return;
    }

    setLoadingTopics(true);
    setTopics([]);

    try {
      const response = await api.get(`/topics/course/${courseId}`);
      setTopics(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to load topics for this course."
      );
    } finally {
      setLoadingTopics(false);
    }
  };

  const handleCourseChange = async (event) => {
    const courseId = event.target.value;

    setSelectedCourse(courseId);
    setSelectedTopic("");
    setError("");

    await fetchTopics(courseId);
  };

  const startNewChat = () => {
    setActiveConversationId(null);
    setMessages([]);
    setInput("");
    setSelectedCourse("");
    setSelectedTopic("");
    setTopics([]);
    setError("");
  };

  const openConversation = async (conversationId) => {
    setLoadingConversation(true);
    setError("");

    try {
      const response = await api.get(
        `/ai-tutor/conversations/${conversationId}`
      );

      const conversation = response.data;

      setActiveConversationId(conversation.id);
      setMessages(conversation.messages || []);
      setSelectedCourse(
        conversation.course_id ? String(conversation.course_id) : ""
      );
      setSelectedTopic(
        conversation.topic_id ? String(conversation.topic_id) : ""
      );

      if (conversation.course_id) {
        const topicResponse = await api.get(
          `/topics/course/${conversation.course_id}`
        );
        setTopics(topicResponse.data);
      } else {
        setTopics([]);
      }
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to open this conversation."
      );
    } finally {
      setLoadingConversation(false);
    }
  };

  const deleteConversation = async (conversationId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this conversation?"
    );

    if (!confirmed) return;

    try {
      await api.delete(`/ai-tutor/conversations/${conversationId}`);

      setConversations((previous) =>
        previous.filter((item) => item.id !== conversationId)
      );

      if (activeConversationId === conversationId) {
        startNewChat();
      }
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to delete this conversation."
      );
    }
  };

  const sendMessage = async (event) => {
    event?.preventDefault();

    const message = input.trim();

    if (!message || sending) return;

    if (message.length > 10000) {
      setError("Your message cannot exceed 10,000 characters.");
      return;
    }

    const temporaryMessage = {
      id: `temporary-${Date.now()}`,
      role: "user",
      content: message,
      created_at: new Date().toISOString(),
    };

    setMessages((previous) => [...previous, temporaryMessage]);
    setInput("");
    setSending(true);
    setError("");

    try {
      const response = await api.post("/ai-tutor/chat", {
        message,
        conversation_id: activeConversationId,
        course_id: selectedCourse ? Number(selectedCourse) : null,
        topic_id: selectedTopic ? Number(selectedTopic) : null,
      });

      const data = response.data;

      setActiveConversationId(data.conversation_id);

      setMessages((previous) => [
        ...previous.filter((item) => item.id !== temporaryMessage.id),
        data.user_message,
        data.assistant_message,
      ]);

      await fetchHistory();
    } catch (err) {
      setMessages((previous) =>
        previous.filter((item) => item.id !== temporaryMessage.id)
      );

      setInput(message);

      setError(
        err.response?.data?.detail ||
          "Unable to send your message. Please try again."
      );
    } finally {
      setSending(false);
    }
  };

  const handlePromptClick = (prompt) => {
    setInput(prompt);
  };

  return (
    <DashboardLayout
      title="AI Tutor"
      subtitle="Your personal learning companion, ready to help you understand more."
    >
      <div className="ai-tutor-page">

        <aside className="ai-tutor-history">
          <button
            type="button"
            className="ai-tutor-new-chat"
            onClick={startNewChat}
          >
            <Plus size={19} />
            New Chat
          </button>

          <div className="ai-tutor-history-heading">
            <MessageSquare size={17} />
            <span>Recent Conversations</span>
          </div>

          <div className="ai-tutor-history-list">
            {loading ? (
              <p className="ai-tutor-muted">Loading conversations...</p>
            ) : conversations.length === 0 ? (
              <p className="ai-tutor-muted">
                Your conversations will appear here.
              </p>
            ) : (
              conversations.map((conversation) => (
                <div
                  key={conversation.id}
                  className={`ai-tutor-history-item ${
                    activeConversationId === conversation.id
                      ? "active"
                      : ""
                  }`}
                >
                  <button
                    type="button"
                    className="ai-tutor-history-open"
                    onClick={() => openConversation(conversation.id)}
                  >
                    <MessageSquare size={16} />
                    <span>{conversation.title}</span>
                  </button>

                  <button
                    type="button"
                    className="ai-tutor-delete-chat"
                    onClick={() => deleteConversation(conversation.id)}
                    aria-label="Delete conversation"
                    title="Delete conversation"
                  >
                    <Trash2 size={15} />
                  </button>
                </div>
              ))
            )}
          </div>
        </aside>

        <section className="ai-tutor-chat">

          <div className="ai-tutor-context">
            <div className="ai-tutor-context-label">
              <GraduationCap size={18} />
              <span>Learning Context</span>
            </div>

            <div className="ai-tutor-context-selectors">
              <select
                value={selectedCourse}
                onChange={handleCourseChange}
                disabled={isExistingConversation || loading}
                aria-label="Select course"
              >
                <option value="">General Learning</option>
                {courses.map((course) => (
                  <option key={course.id} value={course.id}>
                    {course.title}
                  </option>
                ))}
              </select>

              <select
                value={selectedTopic}
                onChange={(event) => setSelectedTopic(event.target.value)}
                disabled={
                  !selectedCourse ||
                  loadingTopics ||
                  isExistingConversation
                }
                aria-label="Select topic"
              >
                <option value="">
                  {loadingTopics ? "Loading topics..." : "All Topics"}
                </option>

                {topics.map((topic) => (
                  <option key={topic.id} value={topic.id}>
                    {topic.sequence_number
                      ? `${topic.sequence_number}. `
                      : ""}
                    {topic.title}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {error && (
            <div className="ai-tutor-error" role="alert">
              <AlertCircle size={18} />
              <span>{error}</span>
              <button
                type="button"
                onClick={() => setError("")}
                aria-label="Dismiss error"
              >
                ×
              </button>
            </div>
          )}

          <div className="ai-tutor-messages">
            {loadingConversation ? (
              <div className="ai-tutor-state">
                <LoaderCircle className="ai-tutor-spinner" size={32} />
                <p>Opening your conversation...</p>
              </div>
            ) : messages.length === 0 ? (
              <div className="ai-tutor-welcome">
                <div className="ai-tutor-welcome-icon">
                  <Bot size={38} />
                  <Sparkles size={17} />
                </div>

                <span className="ai-tutor-eyebrow">
                  YOUR AI LEARNING COMPANION
                </span>

                <h2>What would you like to learn today?</h2>

                <p>
                  Ask questions, understand difficult concepts, explore
                  examples, and improve your technical knowledge.
                </p>

                <div className="ai-tutor-prompts">
                  {SUGGESTED_PROMPTS.map((item) => {
                    const Icon = item.icon;

                    return (
                      <button
                        type="button"
                        className="ai-tutor-prompt-card"
                        key={item.title}
                        onClick={() => handlePromptClick(item.prompt)}
                      >
                        <Icon size={21} />
                        <span>{item.title}</span>
                        <small>{item.prompt}</small>
                      </button>
                    );
                  })}
                </div>
              </div>
            ) : (
              <div className="ai-tutor-message-list">
                {messages.map((message) => (
                  <article
                    key={message.id}
                    className={`ai-tutor-message ${
                      message.role === "user"
                        ? "user-message"
                        : "assistant-message"
                    }`}
                  >
                    <div className="ai-tutor-message-avatar">
                      {message.role === "user" ? (
                        <GraduationCap size={19} />
                      ) : (
                        <Bot size={19} />
                      )}
                    </div>

                    <div className="ai-tutor-message-content">
                      <span className="ai-tutor-message-author">
                        {message.role === "user" ? "You" : "AI Tutor"}
                      </span>

                      <div className="ai-tutor-markdown">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                          {message.content}
                        </ReactMarkdown>
                      </div>
                    </div>
                  </article>
                ))}

                {sending && (
                  <div className="ai-tutor-thinking">
                    <Bot size={19} />
                    <span>AI Tutor is thinking...</span>
                    <LoaderCircle size={16} className="ai-tutor-spinner" />
                  </div>
                )}
              </div>
            )}
          </div>

          <form className="ai-tutor-composer" onSubmit={sendMessage}>
            <textarea
              value={input}
              onChange={(event) => setInput(event.target.value)}
              placeholder="Ask your AI Tutor anything..."
              rows={2}
              maxLength={10000}
              disabled={sending || loadingConversation}
              onKeyDown={(event) => {
                if (
                  event.key === "Enter" &&
                  !event.shiftKey &&
                  !event.nativeEvent.isComposing
                ) {
                  event.preventDefault();
                  sendMessage(event);
                }
              }}
            />

            <div className="ai-tutor-composer-footer">
              <span>Press Enter to send · Shift + Enter for a new line</span>

              <button
                type="submit"
                disabled={!input.trim() || sending}
                aria-label="Send message"
              >
                {sending ? (
                  <LoaderCircle size={19} className="ai-tutor-spinner" />
                ) : (
                  <Send size={19} />
                )}
              </button>
            </div>
          </form>

        </section>
      </div>
    </DashboardLayout>
  );
}

export default AITutor;

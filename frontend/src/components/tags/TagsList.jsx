import "./TagsList.css";

export default function TagsList({ tags }) {
  if (!tags || tags.trim() === "") return null;

  const tagList = tags
    .split(",")
    .map((tag) => tag.trim())
    .filter((tag) => tag.length > 0);

  if (tagList.length === 0) return null;

  return (
    <div className="tags-list">
      {tagList.map((tag, index) => (
        <span key={index} className="tag">
          {tag}
        </span>
      ))}
    </div>
  );
}

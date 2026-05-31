import "./DifficultyBadge.css";

export default function DifficultyBadge({ difficulty }) {
  return (
    <span className={`difficulty-badge difficulty-${difficulty?.toLowerCase()}`}>
      {difficulty}
    </span>
  );
}

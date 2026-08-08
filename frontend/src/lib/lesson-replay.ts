export interface ReplayExerciseState {
  correct_answer: string
  user_answer: string | null
  score: number | null
  feedback: string | null
}

export function resetExercisesForReplay<T extends ReplayExerciseState>(
  exercises: T[]
): T[] {
  return exercises.map((exercise) => ({
    ...exercise,
    user_answer: null,
    score: null,
    feedback: null,
  }))
}

export function answerReplayExercise<T extends ReplayExerciseState>(
  exercise: T,
  answer: string
): T {
  const normalizedAnswer = answer.trim().toLocaleLowerCase()
  const normalizedCorrect = exercise.correct_answer.trim().toLocaleLowerCase()
  const correct = normalizedAnswer === normalizedCorrect

  return {
    ...exercise,
    user_answer: answer,
    score: correct ? 1 : 0,
    feedback: correct
      ? 'Correct.'
      : `The answer is ${exercise.correct_answer}.`,
  }
}

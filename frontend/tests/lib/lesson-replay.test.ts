import { describe, expect, it } from 'vitest'
import {
  answerReplayExercise,
  resetExercisesForReplay,
} from '@/lib/lesson-replay'

const completedExercise = {
  id: 7,
  correct_answer: 'Unjani?',
  user_answer: 'Molo!',
  score: 0,
  feedback: 'Try again.',
}

describe('lesson replay helpers', () => {
  it('clears answers without changing the original completed exercise', () => {
    const [replay] = resetExercisesForReplay([completedExercise])

    expect(replay).toEqual({
      ...completedExercise,
      user_answer: null,
      score: null,
      feedback: null,
    })
    expect(completedExercise.score).toBe(0)
  })

  it('checks a replay answer locally without requiring a new API attempt', () => {
    const replay = answerReplayExercise(completedExercise, '  UNJANI? ')

    expect(replay.user_answer).toBe('  UNJANI? ')
    expect(replay.score).toBe(1)
    expect(replay.feedback).toBe('Correct.')
  })
})

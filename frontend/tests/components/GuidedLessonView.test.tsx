import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import {
  GuidedLessonView,
  type GuidedLearningFlow,
} from '@/components/lessons/GuidedLessonView'

vi.mock('@/components/ui/AudioPlayer', () => ({
  AudioPlayer: ({ text }: { text: string }) => (
    <button type="button">Listen to {text}</button>
  ),
}))

const flow: GuidedLearningFlow = {
  version: 1,
  day: 1,
  goal: 'Greet one person and ask how they are.',
  coach_note: 'Greeting people first matters.',
  phrases: [
    {
      text: 'Molo!',
      translation: 'Hello!',
      chunks: 'Mo·lo',
      usage: 'Use this for one person.',
    },
  ],
  dialogue: [
    { speaker: 'You', text: 'Molo!', translation: 'Hello!' },
  ],
}

const exercise = {
  id: 1,
  native_question: 'What does “Molo” mean?',
  question: 'Kuthetha ukuthini?',
  options: ['Hello!', 'Goodbye!'],
  correct_answer: 'Hello!',
  user_answer: null,
  score: null,
  native_explanation: 'Molo means hello.',
  feedback: null,
}

function renderView() {
  const onAnswerChange = vi.fn()
  const onSubmitAnswer = vi.fn(async () => {})
  render(
    <GuidedLessonView
      flow={flow}
      nativeTitle="Your first conversation"
      xhosaTitle="Incoko yakho yokuqala"
      exercises={[exercise]}
      currentExercise={0}
      answer=""
      evaluating={false}
      completing={false}
      isReview={false}
      submitError={false}
      onAnswerChange={onAnswerChange}
      onSubmitAnswer={onSubmitAnswer}
      onExerciseChange={vi.fn()}
      onComplete={vi.fn(async () => {})}
      onExit={vi.fn()}
    />
  )
  return { onAnswerChange, onSubmitAnswer }
}

describe('GuidedLessonView', () => {
  it('teaches one translated, playable phrase at a time', () => {
    renderView()

    expect(screen.getByText(flow.goal)).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }))

    expect(screen.getByText('Molo!')).toBeInTheDocument()
    expect(screen.getByText('Hello!')).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: 'Listen to Molo!' })
    ).toBeInTheDocument()
    expect(screen.queryByText('Greeting people first matters.')).toBeNull()
  })

  it('requires an attempt from memory before revealing choices', () => {
    const { onAnswerChange } = renderView()

    fireEvent.click(screen.getByRole('button', { name: 'Continue' }))
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }))
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }))
    fireEvent.click(screen.getByRole('button', { name: 'Start recall' }))

    expect(screen.getByText(exercise.native_question)).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Hello!' })).toBeNull()
    fireEvent.click(
      screen.getByRole('button', { name: 'I tried · show choices' })
    )
    fireEvent.click(screen.getByRole('button', { name: 'Hello!' }))
    expect(onAnswerChange).toHaveBeenCalledWith('Hello!')
  })
})

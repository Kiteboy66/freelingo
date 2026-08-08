import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import {
  GuidedLessonView,
  type GuidedLearningFlow,
} from '@/components/lessons/GuidedLessonView'

vi.mock('@/components/ui/AudioPlayer', () => ({
  AudioPlayer: ({
    text,
    label,
    audioUrl,
  }: {
    text: string
    label?: string
    audioUrl?: string
  }) => (
    <button type="button" data-audio-url={audioUrl}>
      {label ?? `Listen to ${text}`}
    </button>
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
  dialogue: [{ speaker: 'You', text: 'Molo!', translation: 'Hello!' }],
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

function renderView(answer = '') {
  const onAnswerChange = vi.fn()
  const onSubmitAnswer = vi.fn(async () => {})
  render(
    <GuidedLessonView
      flow={flow}
      nativeTitle="Your first conversation"
      xhosaTitle="Incoko yakho yokuqala"
      exercises={[exercise]}
      currentExercise={0}
      answer={answer}
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

  it('uses two human recordings and an honest sound guide for Unjani', () => {
    const unjaniFlow: GuidedLearningFlow = {
      ...flow,
      phrases: [
        {
          text: 'Unjani?',
          translation: 'How are you? (one person)',
          chunks: 'Un·ja·ni',
          usage: 'Ask this after saying hello.',
        },
      ],
    }

    render(
      <GuidedLessonView
        flow={unjaniFlow}
        nativeTitle="Your first conversation"
        xhosaTitle="Incoko yakho yokuqala"
        exercises={[exercise]}
        currentExercise={0}
        answer=""
        evaluating={false}
        completing={false}
        isReview={false}
        submitError={false}
        onAnswerChange={vi.fn()}
        onSubmitAnswer={vi.fn(async () => {})}
        onExerciseChange={vi.fn()}
        onComplete={vi.fn(async () => {})}
        onExit={vi.fn()}
      />
    )

    fireEvent.click(screen.getByRole('button', { name: 'Continue' }))

    expect(screen.getByText('Native speaker 1')).toHaveAttribute(
      'data-audio-url',
      '/audio/xh/native/unjani-speaker-1.mp3'
    )
    expect(screen.getByText('Native speaker 2')).toHaveAttribute(
      'data-audio-url',
      '/audio/xh/native/unjani-speaker-2.mp3'
    )
    expect(screen.getByText('Build the word')).toBeInTheDocument()
    expect(screen.getByText('u · nja · ni')).toBeInTheDocument()
    expect(screen.queryByText('Say it in parts')).toBeNull()
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

  it('submits the selected answer without forwarding the click event', () => {
    const { onSubmitAnswer } = renderView('Hello!')

    fireEvent.click(screen.getByRole('button', { name: 'Continue' }))
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }))
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }))
    fireEvent.click(screen.getByRole('button', { name: 'Start recall' }))
    fireEvent.click(
      screen.getByRole('button', { name: 'I tried · show choices' })
    )
    fireEvent.click(screen.getByRole('button', { name: 'Check answer' }))

    expect(onSubmitAnswer).toHaveBeenCalledWith()
  })

  it('labels a replay clearly and finishes without completing twice', () => {
    const onComplete = vi.fn(async () => {})
    const onExit = vi.fn()
    const replayExercise = { ...exercise, user_answer: 'Hello!', score: 1 }

    render(
      <GuidedLessonView
        flow={flow}
        nativeTitle="Your first conversation"
        xhosaTitle="Incoko yakho yokuqala"
        exercises={[replayExercise]}
        currentExercise={0}
        answer="Hello!"
        evaluating={false}
        completing={false}
        isReview={false}
        isReplay
        submitError={false}
        onAnswerChange={vi.fn()}
        onSubmitAnswer={vi.fn(async () => {})}
        onExerciseChange={vi.fn()}
        onComplete={onComplete}
        onExit={onExit}
      />
    )

    expect(
      screen.getByText('Practice replay · your completed progress is kept')
    ).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }))
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }))
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }))
    fireEvent.click(screen.getByRole('button', { name: 'Start recall' }))
    fireEvent.click(screen.getByRole('button', { name: 'Finish practice' }))

    expect(onExit).toHaveBeenCalledOnce()
    expect(onComplete).not.toHaveBeenCalled()
  })
})

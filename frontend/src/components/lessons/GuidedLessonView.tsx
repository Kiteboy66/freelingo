'use client'

import { useEffect, useMemo, useState } from 'react'
import { AudioPlayer } from '@/components/ui/AudioPlayer'
import { getXhosaPronunciation } from '@/lib/xhosa-pronunciation'

export interface GuidedPhrase {
  text: string
  translation: string
  chunks: string
  usage: string
}

export interface GuidedDialogueLine {
  speaker: string
  text: string
  translation: string
}

export interface GuidedLearningFlow {
  version: number
  day: number
  goal: string
  coach_note: string
  phrases: GuidedPhrase[]
  dialogue: GuidedDialogueLine[]
}

interface GuidedExercise {
  id: number
  native_question: string | null
  question: string
  options: string[] | null
  correct_answer: string
  user_answer: string | null
  score: number | null
  native_explanation: string | null
  feedback: string | null
}

interface GuidedLessonViewProps {
  flow: GuidedLearningFlow
  nativeTitle: string
  xhosaTitle: string
  exercises: GuidedExercise[]
  currentExercise: number
  answer: string
  evaluating: boolean
  completing: boolean
  isReview: boolean
  isReplay?: boolean
  submitError: boolean
  onAnswerChange: (answer: string) => void
  onSubmitAnswer: () => Promise<void>
  onExerciseChange: (index: number) => void
  onComplete: () => Promise<void>
  onExit: () => void
}

type TeachingStep =
  | { type: 'goal' }
  | { type: 'phrase'; phrase: GuidedPhrase; index: number }
  | { type: 'dialogue' }
  | { type: 'coach' }

export function GuidedLessonView({
  flow,
  nativeTitle,
  xhosaTitle,
  exercises,
  currentExercise,
  answer,
  evaluating,
  completing,
  isReview,
  isReplay = false,
  submitError,
  onAnswerChange,
  onSubmitAnswer,
  onExerciseChange,
  onComplete,
  onExit,
}: GuidedLessonViewProps) {
  const teachingSteps = useMemo<TeachingStep[]>(
    () => [
      { type: 'goal' },
      ...flow.phrases.map(
        (phrase, index): TeachingStep => ({ type: 'phrase', phrase, index })
      ),
      { type: 'dialogue' },
      { type: 'coach' },
    ],
    [flow.phrases]
  )
  const [stepIndex, setStepIndex] = useState(0)
  const [inPractice, setInPractice] = useState(false)
  const [showChoices, setShowChoices] = useState(isReview)
  const exercise = exercises[currentExercise]
  const evaluated = exercise?.score !== null && exercise?.score !== undefined
  const correct = (exercise?.score ?? 0) >= 1
  const totalStages = teachingSteps.length + exercises.length
  const currentStage = inPractice
    ? teachingSteps.length + currentExercise + 1
    : stepIndex + 1

  useEffect(() => {
    setShowChoices(isReview)
  }, [currentExercise, isReview])

  function goForward() {
    if (stepIndex < teachingSteps.length - 1) {
      setStepIndex((value) => value + 1)
      return
    }
    setInPractice(true)
  }

  function goBack() {
    if (inPractice) {
      if (currentExercise > 0) {
        onExerciseChange(currentExercise - 1)
      } else {
        setInPractice(false)
        setStepIndex(teachingSteps.length - 1)
      }
      return
    }
    if (stepIndex > 0) setStepIndex((value) => value - 1)
  }

  function nextPractice() {
    if (currentExercise < exercises.length - 1) {
      onExerciseChange(currentExercise + 1)
    }
  }

  const step = teachingSteps[stepIndex]
  const phrasePronunciation =
    !inPractice && step.type === 'phrase'
      ? getXhosaPronunciation(step.phrase.text)
      : undefined

  return (
    <main className="mx-auto w-full max-w-3xl px-4 py-5 sm:px-6 sm:py-8">
      <header className="border-fl-border bg-fl-surface border">
        <div className="border-fl-border flex items-center justify-between gap-4 border-b px-5 py-3">
          <p className="text-fl-muted-2 font-mono text-xs tracking-widest uppercase">
            Day {flow.day} of 14
          </p>
          <button
            type="button"
            onClick={onExit}
            className="text-fl-muted-3 hover:text-fl-fg px-2 font-mono text-xl"
            aria-label="Exit lesson"
          >
            ×
          </button>
        </div>
        <div className="px-5 py-4">
          <h1 className="text-fl-fg text-xl font-bold sm:text-2xl">
            {nativeTitle}
          </h1>
          <p className="text-fl-muted-3 mt-1">isiXhosa: {xhosaTitle}</p>
          <div className="bg-fl-border mt-4 h-1 overflow-hidden">
            <div
              className="bg-fl-accent h-full transition-all"
              style={{ width: `${(currentStage / totalStages) * 100}%` }}
            />
          </div>
          <p className="text-fl-muted-3 mt-2 font-mono text-xs">
            Step {currentStage} of {totalStages}
          </p>
          {isReplay && (
            <p className="text-fl-accent mt-2 font-mono text-xs tracking-widest uppercase">
              Practice replay · your completed progress is kept
            </p>
          )}
        </div>
      </header>

      <section className="border-fl-border bg-fl-surface mt-4 min-h-[430px] border p-5 sm:p-8">
        {!inPractice && step.type === 'goal' && (
          <div className="flex min-h-[350px] flex-col justify-center">
            <p className="text-fl-accent font-mono text-xs font-bold tracking-widest uppercase">
              Today&apos;s result
            </p>
            <h2 className="text-fl-fg mt-4 text-2xl font-bold sm:text-3xl">
              {flow.goal}
            </h2>
            <p className="text-fl-muted-2 mt-5 max-w-xl text-base leading-7">
              You will learn three useful phrases, use them in a short
              conversation, and then recall them without reading.
            </p>
            <p className="text-fl-muted-3 mt-8 font-mono text-xs tracking-widest uppercase">
              About 10 minutes · speak aloud
            </p>
          </div>
        )}

        {!inPractice && step.type === 'phrase' && (
          <div>
            <p className="text-fl-accent font-mono text-xs font-bold tracking-widest uppercase">
              Phrase {step.index + 1} of {flow.phrases.length}
            </p>
            <p className="text-fl-muted-2 mt-4 text-sm">
              1. Listen &nbsp; 2. Say it aloud &nbsp; 3. Listen once more
            </p>
            <div className="border-fl-border bg-fl-bg mt-5 border p-5 sm:p-7">
              <p className="text-fl-fg text-3xl font-bold sm:text-4xl">
                {step.phrase.text}
              </p>
              <p className="text-fl-muted-1 mt-3 text-lg">
                {step.phrase.translation}
              </p>
              <div className="mt-6 flex flex-wrap gap-3">
                {phrasePronunciation ? (
                  phrasePronunciation.recordings.map((recording) => (
                    <AudioPlayer
                      key={recording.url}
                      text={step.phrase.text}
                      audioUrl={recording.url}
                      label={recording.label}
                      size="md"
                      className="px-5 py-3"
                    />
                  ))
                ) : (
                  <AudioPlayer
                    text={step.phrase.text}
                    size="md"
                    className="px-5 py-3"
                  />
                )}
              </div>
              {phrasePronunciation && (
                <p className="text-fl-muted-3 mt-3 text-sm">
                  Human isiXhosa recordings · two speakers ·{' '}
                  <a
                    href={phrasePronunciation.attribution.url}
                    target="_blank"
                    rel="noreferrer"
                    className="underline underline-offset-2"
                  >
                    source
                  </a>
                </p>
              )}
            </div>
            <div className="mt-5 grid gap-3 sm:grid-cols-2">
              <div className="border-fl-border border p-4">
                <p className="text-fl-muted-3 font-mono text-xs tracking-widest uppercase">
                  Build the word
                </p>
                <p className="text-fl-fg mt-2 text-lg">
                  {phrasePronunciation?.wordParts ?? step.phrase.chunks}
                </p>
                <p className="text-fl-muted-2 mt-2 text-sm leading-6">
                  {phrasePronunciation?.soundGuide ??
                    'These are word parts, not an English phonetic spelling. Copy the recording for the real sound.'}
                </p>
              </div>
              <div className="border-fl-border border p-4">
                <p className="text-fl-muted-3 font-mono text-xs tracking-widest uppercase">
                  When to use it
                </p>
                <p className="text-fl-muted-1 mt-2">{step.phrase.usage}</p>
              </div>
            </div>
          </div>
        )}

        {!inPractice && step.type === 'dialogue' && (
          <div>
            <p className="text-fl-accent font-mono text-xs font-bold tracking-widest uppercase">
              Put it together
            </p>
            <h2 className="text-fl-fg mt-3 text-2xl font-bold">
              A short real conversation
            </h2>
            <p className="text-fl-muted-2 mt-2">
              Play every line, then speak the “You” lines yourself.
            </p>
            <div className="mt-5 space-y-3">
              {flow.dialogue.map((line, index) => (
                <div
                  key={`${line.speaker}-${index}`}
                  className={`border-fl-border flex gap-4 border p-4 ${
                    line.speaker === 'You' ? 'bg-fl-accent/5' : 'bg-fl-bg'
                  }`}
                >
                  <div className="min-w-0 flex-1">
                    <p className="text-fl-muted-3 font-mono text-xs tracking-widest uppercase">
                      {line.speaker}
                    </p>
                    <p className="text-fl-fg mt-1 text-xl font-bold">
                      {line.text}
                    </p>
                    <p className="text-fl-muted-2 mt-1">{line.translation}</p>
                  </div>
                  <AudioPlayer
                    text={line.text}
                    audioUrl={
                      getXhosaPronunciation(line.text)?.recordings[0]?.url
                    }
                    size="md"
                  />
                </div>
              ))}
            </div>
          </div>
        )}

        {!inPractice && step.type === 'coach' && (
          <div className="flex min-h-[350px] flex-col justify-center">
            <p className="text-fl-accent font-mono text-xs font-bold tracking-widest uppercase">
              Use it naturally
            </p>
            <h2 className="text-fl-fg mt-4 text-2xl font-bold">
              One thing to remember
            </h2>
            <p className="text-fl-muted-1 mt-5 max-w-xl text-lg leading-8">
              {flow.coach_note}
            </p>
            <p className="text-fl-muted-3 mt-8">
              Next, you will recall the three phrases. Try to answer aloud
              before looking at the choices.
            </p>
          </div>
        )}

        {inPractice && exercise && (
          <div>
            <p className="text-fl-accent font-mono text-xs font-bold tracking-widest uppercase">
              Recall {currentExercise + 1} of {exercises.length}
            </p>
            <h2 className="text-fl-fg mt-4 text-2xl leading-9 font-bold">
              {exercise.native_question || exercise.question}
            </h2>
            {!showChoices && !evaluated ? (
              <div className="border-fl-border bg-fl-bg mt-6 border p-6">
                <p className="text-fl-muted-1 text-lg">
                  Pause. Say your answer aloud from memory.
                </p>
                <button
                  type="button"
                  onClick={() => setShowChoices(true)}
                  className="border-fl-border-2 text-fl-fg hover:bg-fl-surface mt-6 border px-5 py-3 font-mono text-xs font-bold tracking-widest uppercase"
                >
                  I tried · show choices
                </button>
              </div>
            ) : (
              <div className="mt-6 space-y-3">
                {exercise.options?.map((option) => (
                  <button
                    key={option}
                    type="button"
                    disabled={evaluated || isReview}
                    onClick={() => onAnswerChange(option)}
                    className={`border-fl-border block w-full border p-4 text-left text-lg transition-colors ${
                      answer === option
                        ? 'border-fl-accent bg-fl-accent/10 text-fl-fg'
                        : 'text-fl-muted-1 hover:border-fl-border-2'
                    }`}
                  >
                    {option}
                  </button>
                ))}
              </div>
            )}

            {showChoices && !evaluated && !isReview && (
              <button
                type="button"
                onClick={() => void onSubmitAnswer()}
                disabled={!answer || evaluating}
                className="bg-fl-accent text-fl-accent-fg mt-5 w-full px-5 py-3 font-mono text-xs font-bold tracking-widest uppercase disabled:opacity-40"
              >
                {evaluating ? 'Checking…' : 'Check answer'}
              </button>
            )}

            {submitError && (
              <p className="text-fl-error mt-3 text-sm">
                That could not be checked. Please try again.
              </p>
            )}

            {(evaluated || isReview) && (
              <div
                className={`mt-6 border p-5 ${
                  correct
                    ? 'border-green-500/40 bg-green-500/5'
                    : 'border-red-500/40 bg-red-500/5'
                }`}
              >
                <p className="text-fl-fg text-lg font-bold">
                  {correct ? 'Correct.' : `Answer: ${exercise.correct_answer}`}
                </p>
                <p className="text-fl-muted-1 mt-2">
                  {exercise.native_explanation || exercise.feedback}
                </p>
                {!correct && (
                  <AudioPlayer
                    text={exercise.correct_answer}
                    audioUrl={
                      getXhosaPronunciation(exercise.correct_answer)
                        ?.recordings[0]?.url
                    }
                    size="md"
                    className="mt-4"
                  />
                )}
              </div>
            )}
          </div>
        )}
      </section>

      <nav className="mt-4 flex items-center justify-between gap-4">
        <button
          type="button"
          onClick={goBack}
          disabled={!inPractice && stepIndex === 0}
          className="border-fl-border text-fl-muted-1 border px-5 py-3 font-mono text-xs font-bold tracking-widest uppercase disabled:opacity-30"
        >
          Back
        </button>
        {!inPractice ? (
          <button
            type="button"
            onClick={goForward}
            className="bg-fl-accent text-fl-accent-fg px-6 py-3 font-mono text-xs font-bold tracking-widest uppercase"
          >
            {stepIndex === teachingSteps.length - 1
              ? 'Start recall'
              : 'Continue'}
          </button>
        ) : currentExercise < exercises.length - 1 ? (
          <button
            type="button"
            onClick={nextPractice}
            disabled={!evaluated && !isReview}
            className="bg-fl-accent text-fl-accent-fg px-6 py-3 font-mono text-xs font-bold tracking-widest uppercase disabled:opacity-30"
          >
            Next
          </button>
        ) : (
          <button
            type="button"
            onClick={isReview || isReplay ? onExit : onComplete}
            disabled={(!evaluated && !isReview) || completing}
            className="bg-fl-accent text-fl-accent-fg px-6 py-3 font-mono text-xs font-bold tracking-widest uppercase disabled:opacity-30"
          >
            {completing
              ? 'Finishing…'
              : isReview
                ? 'Back to plan'
                : isReplay
                  ? 'Finish practice'
                  : 'Finish lesson'}
          </button>
        )}
      </nav>
    </main>
  )
}

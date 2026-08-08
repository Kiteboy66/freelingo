import { describe, expect, it } from 'vitest'
import { getXhosaPronunciation } from '@/lib/xhosa-pronunciation'

describe('getXhosaPronunciation', () => {
  it('finds the native recordings despite punctuation and case', () => {
    const pronunciation = getXhosaPronunciation('UNJANI?')

    expect(pronunciation?.wordParts).toBe('u · nja · ni')
    expect(pronunciation?.recordings).toHaveLength(2)
    expect(pronunciation?.recordings[0].url).toBe(
      '/audio/xh/native/unjani-speaker-1.mp3'
    )
    expect(pronunciation?.attribution.url).toBe('https://openslr.org/32/')
  })

  it('does not claim to have a human recording when none is registered', () => {
    expect(getXhosaPronunciation('Molo!')).toBeUndefined()
  })
})

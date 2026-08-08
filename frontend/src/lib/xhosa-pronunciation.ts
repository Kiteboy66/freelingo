export interface XhosaPronunciation {
  wordParts: string
  soundGuide: string
  attribution: {
    label: string
    url: string
  }
  recordings: Array<{
    url: string
    label: string
  }>
}

const PRONUNCIATIONS: Record<string, XhosaPronunciation> = {
  unjani: {
    wordParts: 'u · nja · ni',
    soundGuide:
      'Keep “nj” together as one sound. Keep the vowels short and clear, then copy the speaker’s pitch and rhythm.',
    attribution: {
      label: 'NWU/Google African Speech Technology corpus (CC BY-SA 4.0)',
      url: 'https://openslr.org/32/',
    },
    recordings: [
      {
        url: '/audio/xh/native/unjani-speaker-1.mp3',
        label: 'Native speaker 1',
      },
      {
        url: '/audio/xh/native/unjani-speaker-2.mp3',
        label: 'Native speaker 2',
      },
    ],
  },
}

function pronunciationKey(text: string): string {
  return text
    .toLocaleLowerCase('xh-ZA')
    .replace(/[!?.,;:]/g, '')
    .replace(/\s+/g, ' ')
    .trim()
}

export function getXhosaPronunciation(
  text: string
): XhosaPronunciation | undefined {
  return PRONUNCIATIONS[pronunciationKey(text)]
}

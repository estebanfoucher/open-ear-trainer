/**
 * Test utilities for React Testing Library
 */

import React, { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';
// import { BrowserRouter } from 'react-router-dom';

// Mock API responses
export const mockExerciseList = [
  {
    id: 'minor_third_major_third_octave_melodic',
    name: 'Minor Third, Major Third, Octave (Melodic)',
    description: 'Learn to identify minor third, major third, and octave intervals',
    difficulty: 3,
    category: 'interval_recognition',
    tags: ['intervals', 'melodic'],
    estimated_time: 30,
    prerequisites: [],
    learning_objectives: ['Identify minor third intervals', 'Identify major third intervals', 'Identify octave intervals'],
    input_type: 'multiple_choice',
    answer_format: 'interval_name',
  },
  {
    id: 'perfect_fourth_fifth_octave_melodic',
    name: 'Perfect Fourth, Perfect Fifth, Octave (Melodic)',
    description: 'Learn to identify perfect fourth, perfect fifth, and octave intervals',
    difficulty: 4,
    category: 'interval_recognition',
    tags: ['intervals', 'melodic'],
    estimated_time: 35,
    prerequisites: [],
    learning_objectives: ['Identify perfect fourth intervals', 'Identify perfect fifth intervals', 'Identify octave intervals'],
    input_type: 'multiple_choice',
    answer_format: 'interval_name',
  },
];

export const mockExerciseData = {
  key: 'C major',
  scale: ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
  progression_audio: null,
  target_audio: '/api/audio/test_interval.wav',
  options: ['minor_third', 'major_third', 'octave'],
  correct_answer: 'major_third',
  context: {
    root_note: 'C-4',
    interval: 'major_third',
    question_number: 1,
  },
};

export const mockAnswerResult = {
  is_correct: true,
  user_answer: 'major_third',
  correct_answer: 'major_third',
  feedback: 'Correct! Well done!',
  hints_used: [],
  time_taken: 5,
};

// Custom render function with providers
interface CustomRenderOptions extends Omit<RenderOptions, 'wrapper'> {
  wrapper?: React.ComponentType<{ children: React.ReactNode }>;
}

const AllTheProviders = ({ children }: { children: React.ReactNode }) => {
  return (
    <div>
      {children}
    </div>
  );
};

const customRender = (
  ui: ReactElement,
  options?: CustomRenderOptions
) => render(ui, { wrapper: AllTheProviders, ...options });

// Mock API functions
export const mockApiCalls = {
  getExercises: jest.fn().mockResolvedValue({ data: mockExerciseList }),
  generateExercise: jest.fn().mockResolvedValue({ data: mockExerciseData }),
  checkAnswer: jest.fn().mockResolvedValue({ data: mockAnswerResult }),
  getExerciseInstructions: jest.fn().mockResolvedValue({
    data: {
      instructions: 'Listen to the interval and select the correct answer.',
      hints: ['Think about the size of the interval', 'Consider the harmonic quality']
    }
  }),
};

// Mock axios
export const mockAxios = {
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  delete: jest.fn(),
  create: jest.fn(() => mockAxios),
  defaults: {
    baseURL: 'http://localhost:8000',
  },
};

// Mock audio functions
export const mockAudio = {
  play: jest.fn().mockResolvedValue(undefined),
  pause: jest.fn(),
  load: jest.fn(),
  addEventListener: jest.fn(),
  removeEventListener: jest.fn(),
  currentTime: 0,
  duration: 2.0,
  paused: true,
  volume: 1,
  src: '',
};

// Test data generators
export const generateMockExercise = (overrides = {}) => ({
  ...mockExerciseList[0],
  ...overrides,
});

export const generateMockExerciseData = (overrides = {}) => ({
  ...mockExerciseData,
  ...overrides,
});

export const generateMockAnswerResult = (overrides = {}) => ({
  ...mockAnswerResult,
  ...overrides,
});

// Custom matchers
export const customMatchers = {
  toBeInTheDocument: (received: any) => {
    const pass = received && received.ownerDocument && received.ownerDocument.body.contains(received);
    return {
      pass,
      message: () => `Expected element ${pass ? 'not ' : ''}to be in the document`,
    };
  },
};

// Helper functions
export const waitForAudioToLoad = async (audio: HTMLAudioElement) => {
  return new Promise((resolve) => {
    if (audio.readyState >= 2) {
      resolve(audio);
    } else {
      audio.addEventListener('canplay', () => resolve(audio), { once: true });
    }
  });
};

export const simulateUserInteraction = {
  click: (element: HTMLElement) => {
    element.click();
  },

  type: (element: HTMLElement, text: string) => {
    if (element instanceof HTMLInputElement || element instanceof HTMLTextAreaElement) {
      element.value = text;
      element.dispatchEvent(new Event('input', { bubbles: true }));
    }
  },

  select: (element: HTMLElement, value: string) => {
    if (element instanceof HTMLSelectElement) {
      element.value = value;
      element.dispatchEvent(new Event('change', { bubbles: true }));
    }
  },
};

// Mock localStorage
export const mockLocalStorage = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};

// Mock sessionStorage
export const mockSessionStorage = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};

// Setup mocks
export const setupMocks = () => {
  // Mock localStorage
  Object.defineProperty(window, 'localStorage', {
    value: mockLocalStorage,
    writable: true,
  });

  // Mock sessionStorage
  Object.defineProperty(window, 'sessionStorage', {
    value: mockSessionStorage,
    writable: true,
  });

  // Mock Audio constructor
  global.Audio = jest.fn(() => mockAudio) as any;

  // Mock fetch
  global.fetch = jest.fn();
};

// Cleanup mocks
export const cleanupMocks = () => {
  jest.clearAllMocks();
  mockLocalStorage.clear();
  mockSessionStorage.clear();
};

// Re-export everything from React Testing Library
export * from '@testing-library/react';
export { customRender as render };

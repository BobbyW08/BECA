import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import axios from 'axios';

interface BECAContextType {
  apiUrl: string;
  mode: 'plan' | 'act';
  setMode: (mode: 'plan' | 'act') => void;
  sendMessage: (message: string) => Promise<any>;
  readFile: (path: string) => Promise<any>;
  getFileTree: () => Promise<any>;
  getDiff: (path: string) => Promise<any>;
  getStatus: () => Promise<any>;
}

const BECAContext = createContext<BECAContextType | undefined>(undefined);

interface BECAProviderProps {
  children: ReactNode;
}

export const BECAProvider: React.FC<BECAProviderProps> = ({ children }) => {
  // Get API URL from environment or default to localhost
  const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
  const [mode, setMode] = useState<'plan' | 'act'>('plan');

  const sendMessage = useCallback(async (message: string) => {
    try {
      const response = await axios.post(`${apiUrl}/api/chat`, {
        message,
        mode,
        history: []
      });
      return response.data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }, [apiUrl, mode]);

  const readFile = useCallback(async (path: string) => {
    try {
      const response = await axios.post(`${apiUrl}/api/files/read`, { path });
      return response.data;
    } catch (error) {
      console.error('Error reading file:', error);
      throw error;
    }
  }, [apiUrl]);

  const getFileTree = useCallback(async () => {
    try {
      const response = await axios.get(`${apiUrl}/api/files/tree`);
      return response.data;
    } catch (error) {
      console.error('Error getting file tree:', error);
      throw error;
    }
  }, [apiUrl]);

  const getDiff = useCallback(async (path: string) => {
    try {
      const response = await axios.post(`${apiUrl}/api/files/diff`, { path });
      return response.data;
    } catch (error) {
      console.error('Error getting diff:', error);
      throw error;
    }
  }, [apiUrl]);

  const getStatus = useCallback(async () => {
    try {
      const response = await axios.get(`${apiUrl}/api/status`);
      return response.data;
    } catch (error) {
      console.error('Error getting status:', error);
      throw error;
    }
  }, [apiUrl]);

  return (
    <BECAContext.Provider
      value={{
        apiUrl,
        mode,
        setMode,
        sendMessage,
        readFile,
        getFileTree,
        getDiff,
        getStatus,
      }}
    >
      {children}
    </BECAContext.Provider>
  );
};

export const useBECA = (): BECAContextType => {
  const context = useContext(BECAContext);
  if (!context) {
    throw new Error('useBECA must be used within a BECAProvider');
  }
  return context;
};

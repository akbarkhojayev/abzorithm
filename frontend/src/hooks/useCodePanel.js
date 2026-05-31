import { useEffect, useState, useMemo, useCallback } from "react";
import { useParams } from "react-router-dom";
import {
  getMasala,
  getProblems,
  getProblemsDetails,
  getTestCase,
} from "../pages/services/app.js";

export function useCodePanel() {
  const { slug } = useParams();
  const [details, setDetails] = useState(null);
  const [index, setIndex] = useState(null);
  const [codeBy, setCodeBy] = useState(null);
  const [testCase, setTestCase] = useState([]);
  const [activeCaseId, setActiveCaseId] = useState(null);
  const [output, setOutput] = useState("");
  const [loadingCoding, setLoadingCoding] = useState(false);
  const [error, setError] = useState(null);

  // Problem details va index olish
  useEffect(() => {
    const fetchProblemDetails = async () => {
      setLoadingCoding(true);
      setError(null);
      try {
        const list = await getProblems();
        if (Array.isArray(list)) {
          const foundIndex = list.findIndex((item) => item.slug === slug);
          if (foundIndex !== -1) setIndex(foundIndex + 1);
        }

        const data = await getProblemsDetails(slug);
        setDetails(data || null);
      } catch (err) {
        setError("Masala yuklanishi uchun xatolik yuz berdi");
        console.error("Error fetching problems:", err);
      } finally {
        setLoadingCoding(false);
      }
    };

    fetchProblemDetails();
  }, [slug]);

  // Code template va test case larni olish
  useEffect(() => {
    if (!details?.id) return;

    const fetchMasalaAndCases = async () => {
      try {
        const languages = details?.languages || details?.language_options;
        const selectedLanguage = languages?.[0] || "python";

        const [masala, cases] = await Promise.all([
          getMasala(details.id, selectedLanguage),
          getTestCase(),
        ]);

        if (masala) {
          setCodeBy({ ...masala, selectedLanguage });
        }

        if (Array.isArray(cases)) {
          setTestCase(cases);
          const filtered = cases.filter(
            (c) => c.problem === details.id && !c.is_hidden
          );
          if (filtered.length > 0) setActiveCaseId(filtered[0].id);
        }
      } catch (err) {
        setError("Kod shablon yuklanishi uchun xatolik yuz berdi");
        console.error("Error fetching template or test cases:", err);
      }
    };

    fetchMasalaAndCases();
  }, [details]);

  // Test case larni filter qilish
  const filteredCases = useMemo(() => {
    return (
      testCase
        ?.filter(
          (item) => item.problem === details?.id && !item.is_hidden
        )
        ?.sort((a, b) => a.order - b.order) || []
    );
  }, [testCase, details?.id]);

  // Aktiv test case
  const activeCase = useMemo(() => {
    return filteredCases.find((item) => item.id === activeCaseId);
  }, [filteredCases, activeCaseId]);

  const changeTestCase = useCallback((caseId) => {
    setActiveCaseId(caseId);
  }, []);

  const clearOutput = useCallback(() => {
    setOutput("");
  }, []);

  return {
    details,
    index,
    codeBy,
    setCodeBy,
    testCase,
    activeCaseId,
    changeTestCase,
    activeCase,
    filteredCases,
    output,
    setOutput,
    loadingCoding,
    error,
    clearOutput,
  };
}

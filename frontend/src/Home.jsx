import LinearProgress from '@mui/material/LinearProgress';
import { writeDownloadedFile } from './utils/utils';
import { useState, useContext } from 'react';
import GlobalContext from "./GlobalContext";
import { SettingsManager } from './SettingsManager';
import { SourceManager } from './SourceManager';

export function Home() {
  const appContext = useContext(GlobalContext);
  const [sourceName, setSourceName] = useState(null);
  const [sha256, setSha256] = useState(null);
  const [rows, setRows] = useState(null);
  const [subjects, setSubjects] = useState([]);
  const [classrooms, setClassrooms] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const start = async (e) => {
    let settings = {
      "source_name": sourceName,
      "file_name": e.fileName,
      "zip_name": e.zipName,
      "document_title": e.documentTitle,
      "subjects": e.selectedSubjects,
      "classrooms": e.selectedClassrooms,
      "number_of_exams": Number(e.numberOfExams),
      "number_of_questions": Number(e.numberOfQuestions),
      "number_on_document": e.numberOnDocument,
      "number_on_questions": e.numberOnQuestions,
      "shuffle_questions": e.shuffleQuestions,
      "shuffle_options": e.shuffleOptions,
      "export_solutions": e.exportSolutions,
      "single_inclusion": e.singleInclusion,
    };

    let response;

    try {
      setIsLoading(true);
      response = await fetch(appContext.GENERATE_EXAMS_PATH, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(settings),
      });
      if (response.ok) {
        await writeDownloadedFile(response, `${e.zipName}.zip`);
      }
    } catch (error) {
      appContext.ERROR_GENERATION();
    } finally {
      setIsLoading(false);
    }
  };

  const downloadTemplate = async () => {
    try {
      const response = await fetch(appContext.DOWNLOAD_TEMPLATE_PATH);

      if (response.ok) {
        await writeDownloadedFile(response, appContext.TEMPLATE_NAME);
      }
    } catch (e) {
      appContext.ERROR_TEMPLATE();
    }
  };

  const uploadSource = async (event) => {
    const formData = new FormData();
    formData.append(appContext.BODY_FIELD_FILE, event.target.files[0]);

    try {
      const response = await fetch(appContext.LOAD_SOURCE_PATH, {
        method: 'POST',
        body: formData,
      });
  
      if (response.ok) {
        const data = await response.json();
        setSha256(data.sha256);
        setSourceName(data.sourceName);
        setRows(data.rows);
        setSubjects(data.subjects);
        setClassrooms(data.classrooms);
      }
    } catch (e) {
      appContext.ERROR_LOAD_SOURCE();
    }
  };


  return (
    <>
      <SourceManager sha256={sha256} rows={rows} downloadTemplate={downloadTemplate} uploadSource={uploadSource} />
      <hr />
      {isLoading && <LinearProgress sx={{ marginTop: 3, marginBottom: 2, marginLeft: 1 }} />}
      <SettingsManager subjects={subjects} classrooms={classrooms} start={start} />
    </>
  )
}

\LoadClass[a4paper,12pt]{article} % Classe du document

%--------------------- Packages ------------------------

\RequirePackage[french]{babel} %Langue du document
\RequirePackage[utf8]{inputenc} %Caractères spéciaux
\RequirePackage[section]{placeins}%Pour placement de section
\RequirePackage[T1]{fontenc} %Quelques lettres qui sont pas inclus dans UTF-8
\RequirePackage{mathtools} %Paquet pour des équations et symboles mathématiques
\RequirePackage{siunitx} %Pour écrire avec la notation scientifique (Ex.: \num{2e+9})
\RequirePackage{float} %Pour placement d'images
\RequirePackage{graphicx} %Paquet pour insérer des images
\RequirePackage[justification=centering]{caption} %Pour les légendes centralisées
\RequirePackage{subcaption}
\RequirePackage{wallpaper}
\RequirePackage{nomencl}
%\makenomenclature
\RequirePackage{fancyhdr}
%\pagestyle{fancy}
%\fancyheadoffset{1cm}
%\setlength{\headheight}{2cm}
\RequirePackage{url}
\RequirePackage[hidelinks]{hyperref}%Paquet pour insérer légendes dans des sous-figures comme Figure 1a, 1b
\RequirePackage[left=2.5cm,right=2.5cm,top=2cm,bottom=3.5cm]{geometry} %Configuration de la page
\RequirePackage{amsmath}
\RequirePackage{longtable}
\RequirePackage{listings}
\RequirePackage{titlesec}
\RequirePackage{makecell}
\RequirePackage{soul}
\RequirePackage{natbib}
\RequirePackage{enumitem}
\RequirePackage{color}
\RequirePackage{tikz}
\RequirePackage{multirow}
\RequirePackage[ruled,vlined]{algorithm2e}
\RequirePackage{adjustbox}

%-------------------- Setup du rapport ----------------------

\renewcommand{\bibsection}{}

\usetikzlibrary{positioning,shapes,arrows}

\setlength{\parindent}{0pt}

\setcounter{secnumdepth}{5}

\setcounter{tocdepth}{5}

\lstdefinestyle{code_style_border}{
  basicstyle=\ttfamily,
  columns=fullflexible,
  frame=single,
  breaklines=true,
  postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space},
  numberstyle=\tiny\color{gray},
  keywordstyle=\color{blue},
  commentstyle=\color{green!50!black},
  stringstyle=\color{purple}
}

\lstdefinestyle{code_style_no_border}{
  basicstyle=\ttfamily,
  columns=fullflexible,
  breaklines=true,
  postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space},
  numberstyle=\tiny\color{gray},
  keywordstyle=\color{blue},
  commentstyle=\color{green!50!black},
  stringstyle=\color{purple}
} 

%-------------------- Commande du rapport ----------------------

\newcommand{\checkmark}{\tikz\fill[scale=0.4](0,.35) -- (.25,0) -- (1,.7) -- (.25,.15) -- cycle;} 

\newcommand{\cours}[1]{\renewcommand{\cours}{#1}}
\newcommand{\sujet}[1]{\renewcommand{\sujet}{#1}}
\newcommand{\titre}[1]{\renewcommand{\titre}{#1}}
\newcommand{\enseignant}[1]{\renewcommand{\enseignant}{#1}}
\newcommand{\eleves}[1]{\renewcommand{\eleves}{#1}}
\newcommand{\logo}[1]{\renewcommand{\logo}{#1}}
\newcommand{\unif}[1]{\renewcommand{\unif}{#1}}

\newcommand{\fairemarges}{
    \makenomenclature
    \pagestyle{fancy}
    \fancyheadoffset{1cm}
    \setlength{\headheight}{2cm}
    \lhead{\includegraphics[scale=0.15]{\logo}} %Affichage de l'image au top de la page
    \rhead{\nouppercase{\leftmark}}
    \rfoot{\thepage}
    \cfoot{\parbox{10cm}{\centering\textit{\titre}}}
}

\newcommand{\fairepagedegarde}{
\begin{titlepage}

	\centering %Centraliser le contenu
	\includegraphics[width=0.5\textwidth]{\logo}\par\vspace{1cm} %Insertion du logo
	{\scshape\LARGE \unif \par} %Nom de l'université
	\vspace{1.5cm}%Espace de 1,5cm
	{\scshape\Large \cours \\ \textbf{\sujet} \par} %sous-titre
	\vspace{1cm}%Espace de 1cm
    \rule{\linewidth}{0.2 mm} \\[0.4 cm]
	{\huge\bfseries \titre \par} \
    \rule{\linewidth}{0.2 mm} \\[1.5 cm]
	\vspace{1cm}%Espace de 1cm
    
	\begin{minipage}{0.5\textwidth} %Minipage pour faire deux colonnes
		\begin{flushleft} \large %Envoyer à gauche
		\emph{\textbf{Élève :}}\\ %Pour le titre au dessus des noms à gauche
        \eleves\\ %Remplacer pour chacun
		\end{flushleft}
	\end{minipage}
	~
	\begin{minipage}{0.4\textwidth}
		\begin{flushleft} \large
		\emph{\textbf{Directeur de projet :}} \\
		 \enseignant \\
		\end{flushleft}
	\end{minipage}\\[4cm]
    
	\vfill
	{\large Année académique 2023 - 2024\par} %Affichage de la date

\end{titlepage}
}

\newcommand{\tabledematieres}{
    \tableofcontents
    \newpage
}

\newcommand{\insererfigure}[4]{
    \begin{figure}[ht]
        \centering
        \includegraphics[scale=#2]{#1}
        \caption{#3}
        \label{fig:#4}
    \end{figure}
}
\newcommand{\insererfiguresideways}[4]{
    \begin{figure}[ht]
        \centering
        \includegraphics[scale=#2, angle=90]{#1}
        \caption{#3}
        \label{fig:#4}
    \end{figure}
}

\newcommand{\myline}[0]{\par\noindent\rule{\textwidth}{0.4pt}\\}

\newcommand{\copybutton}[1]{
    \begin{center}
        \mediabutton[
        jsaction={
        var fld = this.addField("ToCopy", "text", \thepage-1, this.getPageBox({nPage: \thepage-1}));
        fld.value = "#1";
        fld.setFocus();
        app.alert("Copied to Clipboard!");
        app.execMenuItem("Copier");
        app.removeField("ToCopy");
        }
        ]{\fbox{\strut Cliquez ici pour copier le code}}
    \end{center}
}

\newcommand{\highlightref}[1]{\textcolor{cyan}{\ref{#1}}}
\newcommand{\highlightcite}[1]{\textcolor{cyan}{\cite{#1}}}
\newcommand{\highlighthyperref}[2]{\hyperref[#1]{\fcolorbox{cyan}{white}{#2}}}
\newcommand{\highlighthyperrefurl}[2]{\href{#1}{\fcolorbox{cyan}{white}{#2}}}

% Définir la commande \comparefigures
\newcommand{\comparethreefigures}[9]{
      \def\ArgI{#1}%
      \def\ArgII{#2}%
      \def\ArgIII{#3}%
      \def\ArgIV{#4}%
      \def\ArgV{#5}%
      \def\ArgVI{#6}%
      \def\ArgVII{#7}%
      \def\ArgVIII{#8}%
      \def\ArgIX{#9}%
      \comparefigurescreator
}

\newcommand{\comparefigurescreator}[2]{
    \begin{figure}[h!]
        \centering
        \begin{subfigure}[b]{0.46\textwidth}
            \includegraphics[width=\textwidth]{\ArgI}
            \caption{\ArgII}
            \label{fig:\ArgIII}
        \end{subfigure}\hfill
        \begin{subfigure}[b]{0.46\textwidth}
            \includegraphics[width=\textwidth]{\ArgIV}
            \caption{\ArgV}
            \label{fig:\ArgVI}
        \end{subfigure}
        \begin{subfigure}[b]{0.46\textwidth}
            \centering
            \includegraphics[width=\textwidth]{\ArgVII}
            \caption{\ArgVIII}
            \label{fig:\ArgIX}
        \end{subfigure}
        
        
        \caption{Comparaison #1}
        \label{fig:#2}
    \end{figure}
}

% Définir la commande \comparefigures
\newcommand{\comparetwofigures}[8]{
    \begin{figure}[h!]
        \centering
        \begin{subfigure}[b]{0.45\textwidth}
            \includegraphics[width=\textwidth]{#1}
            \caption{#2}
            \label{fig:#3}
        \end{subfigure}
        \hfill
        \begin{subfigure}[b]{0.45\textwidth}
            \includegraphics[width=\textwidth]{#4}
            \caption{#5}
            \label{fig:#6}
        \end{subfigure}
        \caption{Comparaison #7}
        \label{fig:#8}
    \end{figure}
}

\newcommand{\twofigures}[6]{
  \begin{figure}[h!]
    \centering
    \begin{minipage}{0.45\textwidth}
      \centering
      \includegraphics[width=\linewidth]{#1}
      \caption{#2}
      \label{fig:#3}
    \end{minipage}\hfill
    \begin{minipage}{0.45\textwidth}
      \centering
      \includegraphics[width=\linewidth]{#4}
      \caption{#5}
      \label{fig:#6}
    \end{minipage}
  \end{figure}
}
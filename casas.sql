-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 27/08/2025 às 00:11
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `cuidamais`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `casas`
--

CREATE TABLE `casas` (
  `id_casa` int(11) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `endereco` varchar(255) DEFAULT NULL,
  `descricao` text DEFAULT NULL,
  `vagas` int(11) DEFAULT NULL,
  `senha` varchar(255) NOT NULL,
  `criado_em` timestamp NOT NULL DEFAULT current_timestamp(),
  `id_plano` int(11) DEFAULT NULL,
  `imagem` varchar(255) NOT NULL DEFAULT '''default.jpg'''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `casas`
--

INSERT INTO `casas` (`id_casa`, `nome`, `email`, `telefone`, `endereco`, `descricao`, `vagas`, `senha`, `criado_em`, `id_plano`, `imagem`) VALUES
(7, 'Casa do Aconchego', 'adm@casadoaconchego.com.br', '11966252417', 'Rua das Acácias, 123', 'A Casa do Aconchego une a excelência no cuidado com uma infraestrutura completa e adaptada para a terceira idade. Contamos com uma equipe multidisciplinar de enfermagem, fisioterapia e nutrição, garantindo segurança e bem-estar. Nossas instalações oferecem quartos confortáveis, áreas de convivência e jardins para uma rotina tranquila e segura.', 4, 'scrypt:32768:8:1$h0tERcQ0KBUjsuZ5$362f20c5777f4c811e21c07cd2b70b2abb3a9ad1bdbaab83ae2f8ba5f3a270c37ad7ff7cb1a3ce2e191a885da26623a04ac29b0f5f1fc1a275c55879e3e0a610', '2025-08-26 18:46:25', 1, 'Gemini_Generated_Image_on86i5on86i5on86.png'),
(8, 'Vila das Rosas - Residencial Sênior Feminino', 'contato@viladasrosas.com', '(19) 3256-7890', 'Bairro Chácara Primavera, SP', 'A Vila das Rosas é um residencial sênior exclusivo para mulheres, que une o conforto de um lar com a segurança de um cuidado especializado. Nossos espaços são alegres e ensolarados, com um lindo jardim e piscina, ideais para atividades ao ar livre e momentos de convivência. Oferecemos uma rotina rica em bem-estar, com atenção individualizada e o carinho que toda mulher merece. Venha florescer conosco na melhor fase da vida', 5, 'scrypt:32768:8:1$KgjFpA50M5xW3piy$b58fdb928b3db862e7dd43c08bb67dc4fe622d60683b648912398cc605efd06ca3b12fe9113f8a4010350048a552c5462021057ac2ac4cf985c8f21733f07127', '2025-08-26 18:53:46', 2, 'Gemini_Generated_Image_a1op7sa1op7sa1op.png'),
(9, 'Lar Feliz', 'contato@larfeliz.org', '(11) 5555-1234', 'Rua das Margaridas, 300 SP', 'No Lar Feliz, acreditamos que a alegria e o bem-estar são essenciais em todas as fases da vida. Oferecemos um ambiente acolhedor e familiar, com espaços internos amplos e iluminados que se abrem para jardins convidativos. Nossa equipe dedicada promove atividades diárias que estimulam a mente e o corpo, garantindo que cada residente viva com dignidade, felicidade e plena participação', 2, 'scrypt:32768:8:1$czUPjCCpyT0owSYX$edcdde76c66a861cd8498975ddbaceae3ef36d467e05e2674b04cf5b1f89458004c553b9f5b5b49563d312a78e8a0ca0f2859f066608ccda77e16a8e9916543d', '2025-08-26 19:01:41', 1, 'Gemini_Generated_Image_qh4zbuqh4zbuqh4z.png'),
(10, 'Refugio do Bosque', 'refugiobosque@gmail.com', '11990052398', 'Horto Florestal 12333 SP', 'O Refúgio do Bosque é um convite à tranquilidade e ao bem-estar. Com uma arquitetura que privilegia a luz natural e a vista para amplas áreas verdes, oferecemos um ambiente sereno e inspirador. Nossos espaços são projetados para o conforto e a liberdade, onde cada residente pode encontrar seu próprio ritmo, seja em uma leitura tranquila ao lado da janela ou em uma caminhada pelo nosso jardim. Aqui, o cuidado é sinônimo de paz', 5, 'scrypt:32768:8:1$i8UotVdxdQUnM4hg$20cfdd954a75313f9f514e717f85cf9d9827359181202111d3de76bc808f3a3e3ec82c5d78fced6255474917013716a024032d32661ee636eb8a27fb20ae4aa9', '2025-08-26 19:08:06', 1, 'Gemini_Generated_Image_d19onfd19onfd19o.png');

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `casas`
--
ALTER TABLE `casas`
  ADD PRIMARY KEY (`id_casa`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `fk_plano` (`id_plano`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `casas`
--
ALTER TABLE `casas`
  MODIFY `id_casa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `casas`
--
ALTER TABLE `casas`
  ADD CONSTRAINT `fk_plano` FOREIGN KEY (`id_plano`) REFERENCES `planos` (`id_plano`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

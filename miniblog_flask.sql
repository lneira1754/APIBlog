-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 17-07-2025 a las 20:27:57
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `miniblog_flask`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('4298dc60cfb2');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `category`
--

CREATE TABLE `category` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `category`
--

INSERT INTO `category` (`id`, `name`) VALUES
(3, 'Anime'),
(4, 'Clases'),
(5, 'Linux'),
(1, 'programacion');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comment`
--

CREATE TABLE `comment` (
  `id` int(11) NOT NULL,
  `text` text NOT NULL,
  `created_at` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `comment`
--

INSERT INTO `comment` (`id`, `text`, `created_at`, `user_id`, `post_id`) VALUES
(1, 'buena publicacion', '2025-07-13 18:41:35', 1, 1),
(2, 'buena', '2025-07-13 18:49:24', 1, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `post`
--

CREATE TABLE `post` (
  `id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `post`
--

INSERT INTO `post` (`id`, `title`, `content`, `created_at`, `user_id`) VALUES
(1, 'Prueba', 'esta es una prueba', '2025-07-13 18:27:07', 1),
(2, 'logaritmos', 'nada de logaritmos aqui', '2025-07-13 18:28:31', 2),
(3, 'clases de linux', 'Mañana tenemos clases de linux en la sala 7 a las 8', '2025-07-13 18:43:43', 1),
(4, 'tuki', 'nada nada', '2025-07-13 18:48:44', 1),
(5, 'pruba45', 'esta solo es una prueba de cuanto puede guardar el minoblog, nada mas y nada menos, solo se prueba cuanto es lo maximo que se muestra en el index para corregir problemas', '2025-07-17 18:15:04', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `post_category`
--

CREATE TABLE `post_category` (
  `post_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `post_category`
--

INSERT INTO `post_category` (`post_id`, `category_id`) VALUES
(1, 1),
(2, 1),
(3, 4),
(3, 5),
(4, 3),
(5, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(256) NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password_hash`, `is_active`) VALUES
(1, 'kuro', 'kuro@kuro.com', 'scrypt:32768:8:1$IkwnOf9heKCHjIs4$1409895fb28af4c510d2c5e369047b24c90b4ccccfa9f433a482dcabdfd6928ab9e7fbe20eb987a4416a99de8c9c1df36e6aa808cec0b555e607e60043257381', 1),
(2, 'pepe', 'pepe@pepe.com', 'scrypt:32768:8:1$1NKFcL9nvfiYSeAk$6f46774f5282ec06f5f4bfdc5ae82456efea19e97cfa622d54433839c25dcdb1d395805320971a1974e427c758f894a9e136d308cb4f0f4396c04c6e6c144315', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indices de la tabla `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `comment`
--
ALTER TABLE `comment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `post_id` (`post_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `post`
--
ALTER TABLE `post`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `post_category`
--
ALTER TABLE `post_category`
  ADD PRIMARY KEY (`post_id`,`category_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indices de la tabla `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `category`
--
ALTER TABLE `category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `comment`
--
ALTER TABLE `comment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `post`
--
ALTER TABLE `post`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `comment`
--
ALTER TABLE `comment`
  ADD CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`),
  ADD CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Filtros para la tabla `post`
--
ALTER TABLE `post`
  ADD CONSTRAINT `post_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Filtros para la tabla `post_category`
--
ALTER TABLE `post_category`
  ADD CONSTRAINT `post_category_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  ADD CONSTRAINT `post_category_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

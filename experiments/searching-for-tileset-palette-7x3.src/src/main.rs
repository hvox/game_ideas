use image::EncodableLayout;
use itertools::Itertools;
extern crate image;

// miniblob: 64,16,24,8,214,251,104,66,0,208,248,254,255,107,2,0,22,31,223,127,11

const GRID_WIDTH: usize = 7;
const GRID_HEIGHT: usize = 3;
const TILES: [u8; GRID_WIDTH * GRID_HEIGHT] =
	[0, 2, 66, 64, 8, 24, 16, 22, 31, 11, 214, 255, 107, 208, 248, 104, 254, 251, 223, 127, 0];
const FULL_BLOCKS: [&str; 3] = ["░░", "▓▓", "██"];
const NONE_TILE: u8 = 253;
const GRID_SIZE: usize = GRID_WIDTH * GRID_HEIGHT;

fn bit(mask: u8, index: u8) -> bool {
	((mask >> (index - 1)) & 1) != 0
}

fn print_grid(grid: &[u8]) {
	for row in grid.chunks(GRID_WIDTH).rev() {
		let up = row
			.iter()
			.map(|&x| {
				(6..=8).map(|i| FULL_BLOCKS[if bit(x, i) { 2 } else { 0 }]).collect::<String>()
			})
			.collect::<String>();
		let mid = row
			.iter()
			.map(|&x| {
				[4, 5]
					.into_iter()
					.map(|i| FULL_BLOCKS[if bit(x, i) { 2 } else { 0 }])
					.join(FULL_BLOCKS[1])
			})
			.collect::<String>();
		let down = row
			.iter()
			.map(|&x| {
				(1..=3).map(|i| FULL_BLOCKS[if bit(x, i) { 2 } else { 0 }]).collect::<String>()
			})
			.collect::<String>();
		[up, mid, down].into_iter().for_each(|s| println!("{}", s));
	}
}

fn save_grid(name: &str, grid: &[u8]) {
	let tiles_image = image::load_from_memory(include_bytes!("tiles.png")).unwrap().to_rgba8();
	let tiles = tiles_image.as_bytes();
	const TILE_SIZE: usize = 16;
	let mut image = [0u8; GRID_SIZE * TILE_SIZE.pow(2) * 4];
	let w = GRID_WIDTH * TILE_SIZE;
	let source_w = 7 * TILE_SIZE;
	for (y2, row) in grid.chunks(GRID_WIDTH).rev().enumerate() {
		for (x2, tile) in row.into_iter().enumerate() {
			let t = [
				0, 0, 0, 2, 8, 10, 11, 16, 18, 22, 24, 26, 27, 30, 31, 64, 66, 72, 74, 75, 80, 82,
				86, 88, 90, 91, 94, 95, 104, 106, 107, 120, 122, 123, 126, 127, 208, 210, 214, 216,
				218, 219, 222, 223, 248, 250, 251, 254, 255,
			];
			let t = t.iter().enumerate().filter(|(_, mask)| *mask == tile).next().unwrap().0;
			let (x1, y1) = (t % 7, t / 7);
			for dy in 0..TILE_SIZE {
				for dx in 0..TILE_SIZE {
					let i = x2 * TILE_SIZE + dx + (y2 * TILE_SIZE + dy) * w;
					let j = x1 * TILE_SIZE + dx + (y1 * TILE_SIZE + dy) * source_w;
					(0..4).for_each(|k| image[i * 4 + k] = tiles[j * 4 + k]);
				}
			}
		}
	}
	image::save_buffer(
		&std::path::Path::new(name),
		&image,
		(GRID_WIDTH * TILE_SIZE) as u32,
		(GRID_HEIGHT * TILE_SIZE) as u32,
		image::ColorType::Rgba8,
	)
	.unwrap();
}

static mut GRIDS_FOUND: i32 = 0;
fn search() -> i32 {
	fn dfs(i: usize, grid: &mut [u8; GRID_SIZE], tiles: &mut [u8; GRID_SIZE]) -> i32 {
		let x = i % GRID_WIDTH;
		let y = i / GRID_WIDTH;
		if y >= GRID_HEIGHT {
			if continuity_score(grid) > 0 {
				return 0;
			}
			unsafe {
				GRIDS_FOUND += 1;
				println!("\n#{} : {:?}", GRIDS_FOUND, grid);
				let tiles = grid.iter().map(|&x| x.to_string()).join(",");
				save_grid(&format!("grid-{}.png", tiles), grid);
			}
			print_grid(grid);
			// unsafe { if GRIDS_FOUND == 1 { panic!("!") }; }
			return 1;
		}
		if grid[i] != NONE_TILE {
			let tile = grid[i];
			if x > 0 {
				let left = if x > 0 { grid[x - 1 + y * GRID_WIDTH] } else { 0 };
				if bit(tile, 1) != bit(left, 3)
					|| bit(tile, 4) != bit(left, 5)
					|| bit(tile, 6) != bit(left, 8)
				{
					return 0;
				}
			}
			if y > 0 {
				let down = if y > 0 { grid[x + (y - 1) * GRID_WIDTH] } else { 0 };
				if tile & 0b111 != (down >> 5) & 0b111 {
					return 0;
				}
			}
			return dfs(i + 1, grid, tiles);
		}
		let mut result = 0;
		for j in 0..tiles.len() {
			let tile = tiles[j];
			if tile == NONE_TILE {
				continue;
			};
			if x > 0 {
				let left = if x > 0 { grid[x - 1 + y * GRID_WIDTH] } else { 0 };
				if bit(tile, 1) != bit(left, 3)
					|| bit(tile, 4) != bit(left, 5)
					|| bit(tile, 6) != bit(left, 8)
				{
					continue;
				}
			}
			if y > 0 {
				let down = if y > 0 { grid[x + (y - 1) * GRID_WIDTH] } else { 0 };
				if tile & 0b111 != (down >> 5) & 0b111 {
					continue;
				}
			}
			grid[i] = tile;
			tiles[j] = NONE_TILE;
			result += dfs(i + 1, grid, tiles);
			tiles[j] = tile;
		}
		grid[i] = NONE_TILE;
		result
	}

	let mut grid = [NONE_TILE; GRID_SIZE];
	let mut tiles: [u8; GRID_SIZE] = TILES.to_vec().try_into().unwrap();
	dfs(0, &mut grid, &mut tiles)
}

fn continuity_score(grid: &[u8]) -> i32 {
	fn find(grid: &[u8], tile: u8) -> (usize, usize) {
		let i = grid.iter().enumerate().filter(|(_, &t)| t == tile).next().unwrap().0;
		let x = i % GRID_WIDTH;
		let y = i / GRID_WIDTH;
		(x, y)
	}
	let w = GRID_WIDTH;
	let mut score = 0;
	let (x, y) = find(grid, 2);
	score += (y < 2 || grid[x + (y - 1) * w] != 66 || grid[x + (y - 2) * w] != 64) as i32;
	let (x, y) = find(grid, 8);
	score += (x < 2 || grid[x - 1 + y * w] != 24 || grid[x - 2 + y * w] != 16) as i32;
	score
}

fn main() {
	let total = search();
	println!("total = {}", total);
}

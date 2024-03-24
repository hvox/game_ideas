use itertools::Itertools;

const FULL_BLOCKS: [&str; 3] = ["░░", "▓▓", "██"];
const NONE_TILE: u8 = 253;
const TILES: [u8; 49] = [
	0, 0, 0, 2, 8, 10, 11, 16, 18, 22, 24, 26, 27, 30, 31, 64, 66, 72, 74, 75, 80, 82, 86, 88, 90,
	91, 94, 95, 104, 106, 107, 120, 122, 123, 126, 127, 208, 210, 214, 216, 218, 219, 222, 223,
	248, 250, 251, 254, 255,
];

fn bit(mask: u8, index: u8) -> bool {
	((mask >> (index - 1)) & 1) != 0
}

fn print_grid(grid: &[u8]) {
	for row in grid.chunks(7).rev() {
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

#[allow(dead_code)]
fn is_grid_tilable(grid: &[u8]) -> bool {
	for y in 0..4 {
		let row = &grid[y * 7..y * 7 + 4];
		if row[0] & 1 != (row[3] & 2) / 2 || (row[0] & 4) / 4 != (row[3] & 8) / 8 {
			return false;
		}
	}
	for x in 0..4 {
		let col: Vec<u8> = (0..4).map(|y| grid[x + y * 7]).collect();
		if col[3] & 4 != (col[0] & 1) || col[3] & 8 != (col[0] & 2) {
			return false;
		}
	}
	true
}

static mut GRIDS_FOUND: i32 = 0;
fn search() -> i32 {
	fn dfs(i: usize, grid: &mut [u8; 49], tiles: &mut [u8; 49]) -> i32 {
		let x = i % 7;
		let y = i / 7;
		if y == 7 {
			unsafe {
				GRIDS_FOUND += 1;
				println!("#{}  :  {:?}", GRIDS_FOUND, grid);
			}
			print_grid(grid);
			// unsafe { if GRIDS_FOUND == 1 { panic!("!") }; }
			return 1;
		}
		if grid[i] != NONE_TILE {
			return dfs(i + 1, grid, tiles);
		}
		let mut result = 0;
		for j in 0..tiles.len() {
			let tile = tiles[j];
			if tile == NONE_TILE {
				continue;
			};
			let left = if x > 0 { grid[x - 1 + y * 7] } else { 0 };
			if bit(tile, 1) != bit(left, 3)
				|| bit(tile, 4) != bit(left, 5)
				|| bit(tile, 6) != bit(left, 8)
			{
				continue;
			}
			let down = if y > 0 { grid[x + (y - 1) * 7] } else { 0 };
			if bit(tile, 1) != bit(down, 6)
				|| bit(tile, 2) != bit(down, 7)
				|| bit(tile, 3) != bit(down, 8)
			{
				continue;
			}
			grid[i] = tile;
			tiles[j] = NONE_TILE;
			result += dfs(i + 1, grid, tiles);
			tiles[j] = tile;
		}
		grid[i] = NONE_TILE;
		result
	}

	let mut grid = [NONE_TILE; 49];
	let mut tiles: [u8; 49] = TILES.to_vec().try_into().unwrap();
	[(6, 0), (42, 0), (48, 0)].into_iter().for_each(|(i, tile)| {
		grid[i] = tile;
		tiles = tiles
			.into_iter()
			.map(|x| if x != tile { x } else { NONE_TILE })
			.collect::<Vec<u8>>()
			.try_into()
			.unwrap();
	});
	dfs(0, &mut grid, &mut tiles)
}

fn main() {
	search();
}
